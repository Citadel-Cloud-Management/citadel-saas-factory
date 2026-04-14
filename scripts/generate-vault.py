#!/usr/bin/env python3
"""Generate Obsidian vault notes for all 265 agents from .claude/agents/_registry.yaml.

Idempotent: safe to re-run. Produces:
  docs/vault/agents/<domain>/<agent-id>.md   — one note per agent
  docs/vault/agents/<domain>/_index.md       — per-domain index
  docs/vault/agents/_index.md                — agent root index
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / ".claude" / "agents" / "_registry.yaml"
VAULT_AGENTS = REPO_ROOT / "docs" / "vault" / "agents"

DOMAIN_LABELS = {
    "executive": "Executive & Strategy",
    "marketing": "Marketing & Growth",
    "sales": "Sales & Revenue",
    "customer-success": "Customer Success & Support",
    "product-design": "Product & UI/UX Design",
    "engineering": "Engineering & Backend",
    "frontend": "Frontend & Mobile",
    "devops": "DevOps & Infrastructure",
    "security": "Security & Compliance",
    "data-analytics": "Data & Analytics",
    "qa-testing": "QA & Testing",
    "hr-people": "HR & People Operations",
    "finance": "Finance & Billing",
    "legal": "Legal & Governance",
    "content": "Content & Communications",
}

# Domain → primary rules / skills it relies on (used to generate backlinks).
DOMAIN_RULES = {
    "engineering": ["api-design", "architecture", "code-quality", "error-handling"],
    "frontend": ["frontend", "accessibility", "performance"],
    "devops": ["devops", "monitoring", "secrets"],
    "security": ["security", "secrets", "guardrails"],
    "data-analytics": ["database", "performance"],
    "qa-testing": ["testing", "code-quality"],
    "executive": ["documentation"],
    "marketing": ["documentation"],
    "sales": ["api-design"],
    "customer-success": ["documentation"],
    "product-design": ["accessibility", "frontend"],
    "hr-people": ["documentation"],
    "finance": ["api-design", "security"],
    "legal": ["guardrails", "secrets"],
    "content": ["documentation"],
}


def parse_registry(text: str) -> list[dict]:
    """Minimal YAML parser tailored to the registry's flat structure."""
    agents: list[dict] = []
    current: dict | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("agents:"):
            continue
        m = re.match(r"^\s*-\s*id:\s*(\S+)\s*$", line)
        if m:
            if current:
                agents.append(current)
            current = {"id": m.group(1)}
            continue
        m = re.match(r"^\s*(name|domain|description):\s*(.+)$", line)
        if m and current is not None:
            current[m.group(1)] = m.group(2).strip()
    if current:
        agents.append(current)
    return agents


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", value.lower()).strip("-")


def related_agents(agent: dict, by_domain: dict[str, list[dict]]) -> list[dict]:
    siblings = [a for a in by_domain[agent["domain"]] if a["id"] != agent["id"]]
    return siblings[:5]


def render_agent(agent: dict, by_domain: dict[str, list[dict]]) -> str:
    domain = agent["domain"]
    domain_label = DOMAIN_LABELS.get(domain, domain)
    rules = DOMAIN_RULES.get(domain, [])
    related = related_agents(agent, by_domain)

    related_yaml = "\n".join(f"  - {r['id']}" for r in related) or "  []"
    rules_links = " ".join(f"[[../../../.claude/rules/{r}|{r}]]" for r in rules) or "_none_"
    related_links = "\n".join(f"- [[{r['id']}|{r['name']}]]" for r in related) or "- _no siblings_"

    return f"""---
agent-id: {agent['id']}
name: {agent['name']}
domain: {domain}
domain-label: {domain_label}
model: claude-sonnet-4-6
tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
related-agents:
{related_yaml}
tags:
  - agent
  - domain/{domain}
---

# {agent['name']}

> **Domain:** [[_index|{domain_label}]] · **ID:** `{agent['id']}`

## Purpose

{agent.get('description', '_No description provided._')}

## Domain

This agent belongs to the **{domain_label}** domain. See the [[_index|domain index]] for related agents.

## Related Agents

{related_links}

## Rules This Agent Follows

{rules_links}

## Vault Links

- Domain index: [[_index]]
- Agent registry root: [[../_index|All Agents]]
- Vault home: [[../../_index|Vault Home]]
- Architecture: [[../../architecture/_index|Architecture Index]]
- Memory: [[../../memory/_index|Memory Index]]

## Linked Notes

<!-- Auto-managed by .claude/skills/obsidian-linker — do not edit between markers -->
<!-- linked-notes:start -->
<!-- linked-notes:end -->
"""


def render_domain_index(domain: str, agents: list[dict]) -> str:
    label = DOMAIN_LABELS.get(domain, domain)
    rows = "\n".join(
        f"- [[{a['id']}|{a['name']}]] — {a.get('description', '').splitlines()[0] if a.get('description') else ''}"
        for a in agents
    )
    return f"""---
title: {label}
domain: {domain}
type: domain-index
tags:
  - index
  - domain/{domain}
---

# {label}

**{len(agents)} agents** in this domain.

## Agents

{rows}

## Vault Links

- [[../_index|All Agents]]
- [[../../_index|Vault Home]]
- [[../../architecture/_index|Architecture]]
- [[../../runbooks/_index|Runbooks]]
"""


def render_agents_root(by_domain: dict[str, list[dict]]) -> str:
    lines = ["---", "title: All Agents", "type: index", "tags: [index, agents]", "---", "", "# All Agents", "",
             f"**{sum(len(v) for v in by_domain.values())} agents** across **{len(by_domain)} domains**.", "",
             "## Domains", ""]
    for domain, agents in sorted(by_domain.items()):
        label = DOMAIN_LABELS.get(domain, domain)
        lines.append(f"- [[{domain}/_index|{label}]] ({len(agents)})")
    lines += ["", "## Vault Links", "", "- [[../_index|Vault Home]]",
              "- [[../architecture/_index|Architecture]]",
              "- [[../runbooks/_index|Runbooks]]",
              "- [[../memory/_index|Memory]]",
              "- [[../knowledge-graph/_index|Knowledge Graph]]", ""]
    return "\n".join(lines)


def main() -> None:
    text = REGISTRY.read_text(encoding="utf-8")
    agents = parse_registry(text)
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for a in agents:
        if "domain" not in a:
            continue
        by_domain[a["domain"]].append(a)

    VAULT_AGENTS.mkdir(parents=True, exist_ok=True)
    (VAULT_AGENTS / "_index.md").write_text(render_agents_root(by_domain), encoding="utf-8")

    for domain, group in by_domain.items():
        domain_dir = VAULT_AGENTS / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        (domain_dir / "_index.md").write_text(render_domain_index(domain, group), encoding="utf-8")
        for agent in group:
            (domain_dir / f"{agent['id']}.md").write_text(render_agent(agent, by_domain), encoding="utf-8")

    total = sum(len(v) for v in by_domain.values())
    print(f"Generated {total} agent notes across {len(by_domain)} domains in {VAULT_AGENTS}")


if __name__ == "__main__":
    main()
