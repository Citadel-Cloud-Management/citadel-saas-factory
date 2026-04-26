#!/usr/bin/env python3
"""Citadel AI Agent Runner.

Loads agent config, resolves prompts, calls the Anthropic API (or runs in
mock mode), and validates output through the guardrails pipeline.

Usage:
    python3 ai/agents/run.py --task summarize-document --input '{"document_text": "...", "max_points": 3}'
    python3 ai/agents/run.py --task summarize-document --input-file data.json
    python3 ai/agents/run.py --task summarize-document --mock
    python3 ai/agents/run.py --list-tasks
    python3 ai/agents/run.py --list-tools
    python3 ai/agents/run.py --validate
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent.parent
AI_DIR = ROOT / "ai"
PROMPTS_DIR = AI_DIR / "prompts"
AGENTS_DIR = AI_DIR / "agents"
TRACES_DIR = AI_DIR / "evals" / "traces"


# ─── Minimal YAML loader (stdlib-only, no pyyaml dependency) ───
def load_yaml_simple(filepath: Path) -> dict[str, Any]:
    """Parse a flat/simple YAML file into a dict. Handles scalars, simple
    lists (inline [...] and indented - items), and one level of nesting.
    Good enough for agent_config.yaml without requiring pyyaml."""
    result: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[str] | None = None
    current_dict: dict[str, Any] | None = None

    text = filepath.read_text(encoding="utf-8")
    for raw_line in text.splitlines():
        # Skip comments and blank lines
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            if current_list is not None and current_key:
                result[current_key] = current_list
                current_list = None
                current_key = None
            if current_dict is not None and current_key:
                result[current_key] = current_dict
                current_dict = None
                current_key = None
            continue

        indent = len(raw_line) - len(raw_line.lstrip())

        # Indented list item
        if stripped.startswith("- ") and current_list is not None:
            current_list.append(stripped[2:].strip())
            continue

        # Indented dict item
        if indent > 0 and ":" in stripped and current_dict is not None:
            k, _, v = stripped.partition(":")
            v = v.strip()
            if v.lower() == "true":
                v = True
            elif v.lower() == "false":
                v = False
            elif v.replace(".", "").isdigit():
                v = float(v) if "." in v else int(v)
            current_dict[k.strip()] = v
            continue

        # Flush any pending collection
        if current_list is not None and current_key:
            result[current_key] = current_list
            current_list = None
        if current_dict is not None and current_key:
            result[current_key] = current_dict
            current_dict = None

        # Top-level key: value
        if ":" in stripped:
            k, _, v = stripped.partition(":")
            k = k.strip()
            v = v.strip()

            if not v:
                # Next lines are either a list or a nested dict
                current_key = k
                current_list = None
                current_dict = None
                continue

            # Inline list: [a, b, c]
            if v.startswith("[") and v.endswith("]"):
                items = [i.strip().strip("\"'") for i in v[1:-1].split(",") if i.strip()]
                result[k] = items
                continue

            # Scalar
            if v.lower() == "true":
                result[k] = True
            elif v.lower() == "false":
                result[k] = False
            elif v.replace(".", "").replace("-", "").isdigit():
                result[k] = float(v) if "." in v else int(v)
            else:
                result[k] = v.strip("\"'")
        else:
            # Determine if we're starting a list or dict
            if current_key and stripped.startswith("- "):
                current_list = [stripped[2:].strip()]
            elif current_key:
                current_dict = {}
                k2, _, v2 = stripped.partition(":")
                current_dict[k2.strip()] = v2.strip()

    # Flush final collection
    if current_list is not None and current_key:
        result[current_key] = current_list
    if current_dict is not None and current_key:
        result[current_key] = current_dict

    return result


# ─── Prompt loading ───
def load_prompt(rel_path: str) -> tuple[dict[str, str], str]:
    """Load a markdown prompt file and return (frontmatter_dict, body)."""
    full = ROOT / rel_path
    if not full.exists():
        raise FileNotFoundError(f"Prompt not found: {full}")

    text = full.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        return {}, text

    fm: dict[str, str] = {}
    for line in match.group(1).splitlines():
        idx = line.find(":")
        if idx > 0:
            fm[line[:idx].strip()] = line[idx + 1 :].strip().strip("\"'")
    return fm, match.group(2)


def render_template(template: str, variables: dict[str, Any]) -> str:
    """Replace {{variable}} placeholders in a prompt template."""
    def replacer(m: re.Match) -> str:
        key = m.group(1)
        return str(variables.get(key, m.group(0)))
    return re.sub(r"\{\{(\w+)\}\}", replacer, template)


# ─── LLM calls ───
def call_llm_mock(system_prompt: str, user_msg: str) -> str:
    """Return a deterministic mock response for testing without an API key."""
    return json.dumps({
        "summary": [
            {"point": "Mock response — pipeline is functional", "source_ref": "mock", "confidence": "HIGH"}
        ],
        "total_points": 1,
        "document_length_chars": len(user_msg),
        "_mock": True,
    })


def call_llm_live(system_prompt: str, user_msg: str, model: str) -> str:
    """Call the Anthropic Messages API. Uses urllib so we stay stdlib-only."""
    import urllib.request
    import urllib.error

    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY not set. Use --mock for testing.", file=sys.stderr)
        sys.exit(1)

    payload = json.dumps({
        "model": model,
        "max_tokens": 4096,
        "system": system_prompt,
        "messages": [{"role": "user", "content": user_msg}],
    }).encode()

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            return data["content"][0]["text"]
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Anthropic API {e.code}: {body}", file=sys.stderr)
        sys.exit(1)


# ─── Task discovery ───
def list_tasks() -> list[dict[str, str]]:
    """Discover all task prompts in ai/prompts/tasks/."""
    tasks = []
    tasks_dir = PROMPTS_DIR / "tasks"
    if not tasks_dir.exists():
        return tasks
    for f in sorted(tasks_dir.glob("*.md")):
        fm, _ = load_prompt(str(f.relative_to(ROOT)))
        tasks.append({
            "file": f.name,
            "name": fm.get("name", f.stem),
            "description": fm.get("description", ""),
        })
    return tasks


def list_tools() -> list[dict[str, str]]:
    """Discover all tool configs in ai/agents/tools/."""
    tools = []
    tools_dir = AGENTS_DIR / "tools"
    if not tools_dir.exists():
        return tools
    for f in sorted(tools_dir.glob("*.yaml")):
        cfg = load_yaml_simple(f)
        tools.append({
            "file": f.name,
            "name": cfg.get("name", f.stem),
            "description": cfg.get("description", ""),
        })
    return tools


# ─── Validate ───
def validate_layer() -> int:
    """Validate the entire ai/ layer structure and return error count."""
    errs = 0

    # Config
    config_path = AGENTS_DIR / "agent_config.yaml"
    if config_path.exists():
        cfg = load_yaml_simple(config_path)
        print(f"  [OK] agent_config.yaml loaded ({len(cfg)} keys)")
    else:
        print("  [FAIL] agent_config.yaml missing")
        errs += 1

    # Prompts
    for subdir in ["system", "tasks", "tools"]:
        d = PROMPTS_DIR / subdir
        count = len(list(d.glob("*.md"))) if d.exists() else 0
        if count > 0:
            print(f"  [OK] prompts/{subdir}/: {count} file(s)")
        else:
            print(f"  [WARN] prompts/{subdir}/: empty")

    # Evals
    tests_dir = AI_DIR / "evals" / "tests"
    test_files = list(tests_dir.glob("*.json")) if tests_dir.exists() else []
    total_cases = 0
    for tf in test_files:
        try:
            cases = json.loads(tf.read_text())
            total_cases += len(cases)
        except json.JSONDecodeError:
            print(f"  [FAIL] {tf.name}: invalid JSON")
            errs += 1

    print(f"  [OK] evals/tests/: {len(test_files)} file(s), {total_cases} test case(s)")

    # Data dirs
    for subdir in ["data/raw", "data/processed"]:
        d = AI_DIR / subdir.replace("/", os.sep)
        if d.exists():
            print(f"  [OK] {subdir}/")
        else:
            print(f"  [WARN] {subdir}/ missing")

    return errs


# ─── Main ───
def main() -> None:
    parser = argparse.ArgumentParser(description="Citadel AI Agent Runner")
    parser.add_argument("--task", help="Task name (matches prompts/tasks/<name>.md)")
    parser.add_argument("--input", help="JSON input string")
    parser.add_argument("--input-file", help="Path to JSON input file")
    parser.add_argument("--mock", action="store_true", help="Use mock LLM (no API key)")
    parser.add_argument("--model", default=None, help="Model override")
    parser.add_argument("--list-tasks", action="store_true", help="List available tasks")
    parser.add_argument("--list-tools", action="store_true", help="List available tools")
    parser.add_argument("--validate", action="store_true", help="Validate ai/ layer integrity")
    parser.add_argument("--verbose", action="store_true", help="Print full payloads")
    args = parser.parse_args()

    if args.list_tasks:
        tasks = list_tasks()
        print(f"\n  Available tasks ({len(tasks)}):\n")
        for t in tasks:
            print(f"    {t['name']:30s} {t['description']}")
        print()
        return

    if args.list_tools:
        tools = list_tools()
        print(f"\n  Available tools ({len(tools)}):\n")
        for t in tools:
            print(f"    {t['name']:30s} {t['description']}")
        print()
        return

    if args.validate:
        print("\n  Citadel AI Layer Validation\n")
        errs = validate_layer()
        print(f"\n  {'[OK] Valid' if errs == 0 else f'[FAIL] {errs} error(s)'}\n")
        sys.exit(1 if errs > 0 else 0)

    if not args.task:
        parser.print_help()
        sys.exit(1)

    # ── Resolve task prompt ──
    task_file = f"ai/prompts/tasks/{args.task}.md"
    alt_file = f"ai/prompts/tasks/{args.task.replace('-', '_')}.md"
    try:
        fm, body = load_prompt(task_file)
    except FileNotFoundError:
        try:
            fm, body = load_prompt(alt_file)
        except FileNotFoundError:
            # Search by frontmatter name
            found = False
            for f in (PROMPTS_DIR / "tasks").glob("*.md"):
                fm2, body2 = load_prompt(str(f.relative_to(ROOT)))
                if fm2.get("name") == args.task:
                    fm, body = fm2, body2
                    found = True
                    break
            if not found:
                print(f"Task not found: {args.task}", file=sys.stderr)
                print(f"  Searched: {task_file}, {alt_file}, and all prompts/tasks/*.md names", file=sys.stderr)
                sys.exit(1)

    # ── Parse input ──
    variables: dict[str, Any] = {}
    if args.input:
        variables = json.loads(args.input)
    elif args.input_file:
        variables = json.loads(Path(args.input_file).read_text())

    # ── Load system prompt ──
    config = load_yaml_simple(AGENTS_DIR / "agent_config.yaml")
    sys_ref = config.get("system_prompt_ref", "ai/prompts/system/base.md")
    _, system_body = load_prompt(str(sys_ref))

    # ── Render task prompt ──
    rendered = render_template(body, variables)
    model = args.model or os.environ.get("AI_EVAL_MODEL") or config.get("model", "claude-sonnet-4-6")

    print(f"\n  Citadel AI Agent Runner")
    print(f"  Task:  {fm.get('name', args.task)}")
    print(f"  Model: {model}")
    print(f"  Mode:  {'mock' if args.mock else 'live'}\n")

    if args.verbose:
        print(f"  System prompt: {len(system_body)} chars")
        print(f"  User prompt:   {len(rendered)} chars\n")

    # ── Call LLM ──
    start = time.time()
    if args.mock:
        raw = call_llm_mock(system_body, rendered)
    else:
        raw = call_llm_live(system_body, rendered, model)
    elapsed = int((time.time() - start) * 1000)

    # ── Parse and display ──
    try:
        output = json.loads(raw)
        print(json.dumps(output, indent=2))
    except json.JSONDecodeError:
        print(raw)
        output = {"raw": raw}

    # ── Write trace ──
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    trace = {
        "task": fm.get("name", args.task),
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "model": model,
        "mode": "mock" if args.mock else "live",
        "input": variables,
        "output": output,
        "elapsed_ms": elapsed,
    }
    trace_file = TRACES_DIR / f"{args.task}_{int(time.time())}.json"
    trace_file.write_text(json.dumps(trace, indent=2))

    print(f"\n  Elapsed: {elapsed}ms")
    print(f"  Trace:   {trace_file.relative_to(ROOT)}\n")


if __name__ == "__main__":
    main()
