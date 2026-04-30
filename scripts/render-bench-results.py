#!/usr/bin/env python3
"""Render benchmark JSON results into a Markdown table.

Reads JSON result files from a directory (--input) or stdin,
writes a Markdown report to --out (default: docs/bench-results.md).
"""

import argparse
import json
import sys
from pathlib import Path


def load_results(input_path: str | None) -> list[dict]:
    """Load benchmark results from a directory or stdin."""
    results: list[dict] = []

    if input_path:
        base = Path(input_path)
        if base.is_file():
            results.append(json.loads(base.read_text(encoding="utf-8")))
        elif base.is_dir():
            for f in sorted(base.rglob("*.json")):
                try:
                    results.append(json.loads(f.read_text(encoding="utf-8")))
                except (json.JSONDecodeError, OSError):
                    continue
    else:
        raw = sys.stdin.read().strip()
        if raw:
            try:
                data = json.loads(raw)
                if isinstance(data, list):
                    results.extend(data)
                else:
                    results.append(data)
            except json.JSONDecodeError:
                pass

    return results


def render_markdown(results: list[dict]) -> str:
    """Render a list of benchmark results as a Markdown table."""
    lines = [
        "# Benchmark Results",
        "",
        f"| Engine | Model | Latency (ms) | Tokens | Status |",
        "|--------|-------|-------------|--------|--------|",
    ]

    for r in results:
        engine = r.get("engine", "unknown")
        model = r.get("model", "unknown")
        latency = r.get("latency_ms", "N/A")
        tokens = r.get("tokens", "N/A")
        status = r.get("status", "unknown")
        lines.append(f"| {engine} | {model} | {latency} | {tokens} | {status} |")

    if not results:
        lines.append("| - | No results available | - | - | - |")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render benchmark results as Markdown")
    parser.add_argument(
        "--input",
        default=None,
        help="Directory or file containing JSON benchmark results",
    )
    parser.add_argument(
        "--out",
        default="docs/bench-results.md",
        help="Output Markdown file path",
    )
    args = parser.parse_args()

    results = load_results(args.input)
    markdown = render_markdown(results)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(markdown, encoding="utf-8")


if __name__ == "__main__":
    main()
