#!/usr/bin/env python3
"""
Generate docs/strategy.html from .claude/agents/_registry.yaml.

Produces a dark-themed one-page strategy document with every one of the 265
agents listed individually, multi-engine comparison, Ruflo, Graphify, and the
free toolchain matrix. All HTML entities properly escaped.

Run:
    python scripts/generate-strategy-html.py
"""
from __future__ import annotations

import html
import sys
from collections import OrderedDict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / ".claude" / "agents" / "_registry.yaml"
OUT = ROOT / "docs" / "strategy.html"

DOMAIN_ORDER = [
    ("executive",        "Executive & Strategy",   "#e8a5ff"),
    ("marketing",        "Marketing & Growth",     "#ffa5c8"),
    ("sales",            "Sales & Revenue",        "#ffcf85"),
    ("customer-success", "Customer Success",       "#b5e0ae"),
    ("product-design",   "Product & UI/UX",        "#52c2f0"),
    ("engineering",      "Engineering",            "#4a9fe2"),
    ("frontend",         "Frontend",               "#4a8fe0"),
    ("devops",           "DevOps",                 "#1ac0b6"),
    ("security",         "Security",               "#d83030"),
    ("data-analytics",   "Data & Analytics",       "#89638a"),
    ("qa-testing",       "QA & Testing",           "#afa65d"),
    ("hr-people",        "HR & People",            "#d3577f"),
    ("finance",          "Finance & Billing",      "#64a569"),
    ("legal",            "Legal & Governance",     "#8c8c8c"),
    ("content",          "Content & Comms",        "#dec27d"),
]


def load_agents() -> list[dict]:
    with REGISTRY.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("agents", [])


def group_by_domain(agents: list[dict]) -> OrderedDict[str, list[dict]]:
    buckets: OrderedDict[str, list[dict]] = OrderedDict((k, []) for k, _, _ in DOMAIN_ORDER)
    for a in agents:
        d = a.get("domain", "other")
        buckets.setdefault(d, []).append(a)
    return buckets


def esc(s: str) -> str:
    return html.escape(s or "", quote=True)


def render_domain_table(domain_key: str, label: str, color: str, agents: list[dict]) -> str:
    rows = []
    for i, a in enumerate(agents, start=1):
        rows.append(
            f'        <tr>'
            f'<td class="num">{i:03d}</td>'
            f'<td class="id"><code>{esc(a.get("id", ""))}</code></td>'
            f'<td class="name">{esc(a.get("name", ""))}</td>'
            f'<td class="desc">{esc(a.get("description", ""))}</td>'
            f'</tr>'
        )
    rows_html = "\n".join(rows)
    count = len(agents)
    return f"""
  <section class="domain" id="domain-{esc(domain_key)}">
    <h3><span class="badge" style="background:{color};color:#060810">{esc(label)}</span>
        <span class="count">{count} agents</span></h3>
    <table>
      <thead><tr><th>#</th><th>ID</th><th>Name</th><th>Description</th></tr></thead>
      <tbody>
{rows_html}
      </tbody>
    </table>
  </section>"""


def render() -> str:
    agents = load_agents()
    buckets = group_by_domain(agents)
    total = sum(len(v) for v in buckets.values())

    # Stats row
    stats_cells = "".join(
        f'<div class="stat"><div class="stat-num">{len(buckets.get(k, []))}</div>'
        f'<div class="stat-lbl">{esc(label)}</div></div>'
        for k, label, _ in DOMAIN_ORDER
    )

    domain_sections = "\n".join(
        render_domain_table(k, label, color, buckets.get(k, []))
        for k, label, color in DOMAIN_ORDER
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Citadel SaaS Factory &#x2014; Strategy v3.0</title>
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&amp;family=DM+Mono:wght@400;500&amp;display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #060810;
    --panel: #0e1220;
    --panel2: #151a2e;
    --fg: #e6e9f5;
    --muted: #8b92ab;
    --accent: #5b8dff;
    --accent2: #b5e0ae;
    --border: #1f2540;
  }}
  * {{ box-sizing: border-box; }}
  html, body {{ margin: 0; background: var(--bg); color: var(--fg); font-family: 'Sora', Calibri, Helvetica, sans-serif; font-weight: 300; line-height: 1.55; }}
  code, pre, .id code, .mono {{ font-family: 'DM Mono', Menlo, Consolas, monospace; }}
  .wrap {{ max-width: 1240px; margin: 0 auto; padding: 56px 32px 96px; }}
  header {{ border-bottom: 1px solid var(--border); padding-bottom: 32px; margin-bottom: 48px; }}
  h1 {{ font-size: 44px; font-weight: 700; letter-spacing: -0.02em; margin: 0 0 12px; }}
  h1 .v {{ color: var(--muted); font-weight: 300; font-size: 0.6em; margin-left: 12px; }}
  .tagline {{ color: var(--muted); font-size: 18px; max-width: 780px; }}
  h2 {{ font-size: 28px; font-weight: 600; margin: 56px 0 20px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }}
  h3 {{ font-size: 20px; font-weight: 600; margin: 32px 0 12px; display: flex; align-items: center; gap: 16px; }}
  .badge {{ display: inline-block; padding: 4px 14px; border-radius: 999px; font-size: 13px; font-weight: 600; }}
  .count {{ color: var(--muted); font-size: 14px; font-weight: 400; }}
  .stats {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; margin: 32px 0 48px; }}
  .stat {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 20px 16px; text-align: center; }}
  .stat-num {{ font-size: 32px; font-weight: 700; color: var(--accent2); }}
  .stat-lbl {{ color: var(--muted); font-size: 12px; margin-top: 4px; }}
  .total-stat {{ background: linear-gradient(135deg, #1a2240, #0e1220); border: 1px solid var(--accent); grid-column: span 5; padding: 28px; }}
  .total-stat .stat-num {{ font-size: 56px; color: var(--accent); }}
  .total-stat .stat-lbl {{ font-size: 14px; }}
  table {{ width: 100%; border-collapse: collapse; background: var(--panel); border: 1px solid var(--border); border-radius: 8px; overflow: hidden; font-size: 13px; }}
  th {{ text-align: left; padding: 12px 16px; background: var(--panel2); color: var(--muted); font-weight: 600; border-bottom: 1px solid var(--border); text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; }}
  td {{ padding: 10px 16px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  td.num {{ color: var(--muted); font-family: 'DM Mono', monospace; width: 48px; }}
  td.id code {{ color: var(--accent); font-size: 12px; }}
  td.name {{ font-weight: 500; color: var(--fg); white-space: nowrap; }}
  td.desc {{ color: #bfc5d9; }}
  .domain {{ margin-bottom: 40px; }}
  .tree {{ background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 24px; font-family: 'DM Mono', monospace; font-size: 13px; color: var(--fg); white-space: pre; overflow-x: auto; line-height: 1.8; }}
  .tree .dir {{ color: var(--accent); }}
  .tree .file {{ color: var(--muted); }}
  .engines {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 24px 0; }}
  .engine {{ background: var(--panel); border: 1px solid var(--border); border-radius: 12px; padding: 24px; }}
  .engine h4 {{ margin: 0 0 12px; font-size: 18px; }}
  .engine .price {{ font-size: 28px; font-weight: 700; color: var(--accent2); margin: 8px 0; }}
  .engine ul {{ padding-left: 18px; color: #bfc5d9; margin: 12px 0; }}
  .tools-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 24px 0; }}
  .tool {{ background: var(--panel); border: 1px solid var(--border); border-radius: 8px; padding: 14px 18px; }}
  .tool .tool-name {{ font-weight: 600; color: var(--fg); }}
  .tool .tool-use {{ color: var(--muted); font-size: 12px; }}
  .note {{ background: var(--panel2); border-left: 3px solid var(--accent); padding: 16px 20px; margin: 24px 0; color: #bfc5d9; border-radius: 0 6px 6px 0; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  footer {{ margin-top: 80px; padding-top: 32px; border-top: 1px solid var(--border); color: var(--muted); font-size: 13px; display: flex; justify-content: space-between; flex-wrap: wrap; gap: 12px; }}
</style>
</head>
<body>
<div class="wrap">

<header>
  <h1>Citadel SaaS Factory <span class="v">v3.0</span></h1>
  <p class="tagline">Universal Full-Stack SaaS Production Framework &#x2014; {total} autonomous business agents across 15 domains, three swappable LLM engine backends, Ruflo swarm orchestration, and Graphify knowledge graphs. Clone, configure, deploy on any infrastructure. $0 in software costs.</p>
</header>

<div class="stats">
  <div class="stat total-stat">
    <div class="stat-num">{total}</div>
    <div class="stat-lbl">AUTONOMOUS BUSINESS AGENTS</div>
  </div>
{stats_cells}
</div>

<h2>Agent Fleet &#x2014; All {total} Agents</h2>
<p class="tagline">Every agent listed individually below. Each has a dedicated definition file under <code>.claude/agents/</code> with its own YAML frontmatter, toolset, model assignment, and prompt.</p>
{domain_sections}

<h2>Multi-Engine LLM Backends</h2>
<p class="tagline">Pick the right quality/cost/privacy tradeoff per task. Same <code>.claude/</code> config, three different backends, zero application changes.</p>
<div class="engines">
  <div class="engine">
    <h4>Paid &#x00B7; Anthropic</h4>
    <div class="price">$20&#x2013;200/mo</div>
    <ul>
      <li>Claude Sonnet 4.6 (primary)</li>
      <li>Claude Haiku 4.5 (small/fast)</li>
      <li>~800 ms p50 latency</li>
      <li>100% quality baseline</li>
      <li>Best for production work</li>
    </ul>
    <code>make run-paid</code>
  </div>
  <div class="engine">
    <h4>Free &#x00B7; OpenRouter</h4>
    <div class="price">$0/mo</div>
    <ul>
      <li>Llama 3.3 70B (primary)</li>
      <li>Qwen 3 8B (small/fast)</li>
      <li>~2&#x2013;5 s p50 latency</li>
      <li>~80% quality baseline</li>
      <li>Rate-limited free tier</li>
    </ul>
    <code>make run-free</code>
  </div>
  <div class="engine">
    <h4>Local &#x00B7; Ollama</h4>
    <div class="price">$0/mo</div>
    <ul>
      <li>Qwen 2.5 Coder 32B</li>
      <li>Via y-router proxy</li>
      <li>~300 ms local latency</li>
      <li>Zero data egress</li>
      <li>Air-gapped capable</li>
    </ul>
    <code>make run-local</code>
  </div>
</div>

<h2>.claude/ Folder Structure</h2>
<div class="tree"><span class="dir">.claude/</span>
&#x251C;&#x2500; <span class="file">CLAUDE.md</span>                 &#x2014; project identity, conventions, autonomous-execution
&#x251C;&#x2500; <span class="file">settings.json</span>             &#x2014; hooks, permissions, tool allowlist
&#x251C;&#x2500; <span class="file">settings.md</span>               &#x2014; hook documentation
&#x251C;&#x2500; <span class="dir">agents/</span>                  &#x2014; all {total} agent definitions + _registry.yaml
&#x251C;&#x2500; <span class="dir">skills/</span>                  &#x2014; code-review, security-audit, deploy, testing, llm-wiki, graphify, ...
&#x251C;&#x2500; <span class="dir">commands/</span>                &#x2014; /review, /deploy, /fix-issue, /onboard, /wiki-ingest, ...
&#x251C;&#x2500; <span class="dir">rules/</span>                   &#x2014; 18+ governance files (code-quality, security, architecture, ...)
&#x251C;&#x2500; <span class="dir">templates/</span>               &#x2014; 20 scaffolding templates (.py.tmpl, .tsx.tmpl, .tf.tmpl, ...)
&#x251C;&#x2500; <span class="dir">mcp/</span>                     &#x2014; 8 MCP reference configs (github, postgres, docker, k8s, ...)
&#x251C;&#x2500; <span class="dir">memory/</span>                  &#x2014; project-context, architecture-decisions, agent-learnings
&#x2514;&#x2500; <span class="dir">hooks/</span>                   &#x2014; vault-autolink, graphify pre-tool-use
</div>

<h2>Citadel Mesh &#x00B7; Swarm Orchestration</h2>
<p>Citadel Mesh provides mesh-topology multi-agent coordination across 314 MCP tools. 8 worker types (coder, reviewer, tester, architect, researcher, analyst, optimizer, documenter) with byzantine consensus, auto-remediation, and AgentDB vector memory.</p>
<div class="note">CYCLE_INTERVAL=0 means agents execute in parallel, not on a timer. Byzantine consensus kicks in when two or more agents disagree on a change &#x2014; voting resolves the conflict before any write lands in the working tree.</div>

<h2>Graphify &#x00B7; Codebase Knowledge Graph</h2>
<p>Graphify parses the codebase with Tree-sitter (20 languages), builds a knowledge graph of entities and relationships, and exposes it to Claude via a PreToolUse hook that intercepts every <code>Glob</code>/<code>Grep</code> call. The result: 71&#x00D7; fewer tokens spent on repo exploration. Output lands at <code>graphify-out/GRAPH_REPORT.md</code> and in the Obsidian vault at <code>docs/vault/knowledge-graph/</code>.</p>

<h2>LLM Wiki &#x00B7; Brain Memory</h2>
<p>Citadel uses Andrej Karpathy's LLM Wiki pattern as persistent brain memory. Three layers: immutable <code>raw/</code> sources, LLM-maintained compiled <code>wiki/</code> (entities, concepts, comparisons, contradictions), and a co-evolved <code>SCHEMA.md</code>. Every agent session's valuable output files back into the wiki &#x2014; knowledge compounds across all {total} agents instead of dying with the chat session.</p>

<h2>Free Toolchain</h2>
<p class="tagline">30+ production-grade tools, $0 in software licensing.</p>
<div class="tools-grid">
  <div class="tool"><div class="tool-name">ArgoCD</div><div class="tool-use">GitOps continuous delivery</div></div>
  <div class="tool"><div class="tool-name">K3s</div><div class="tool-use">Lightweight Kubernetes</div></div>
  <div class="tool"><div class="tool-name">Traefik</div><div class="tool-use">Reverse proxy + TLS</div></div>
  <div class="tool"><div class="tool-name">Linkerd</div><div class="tool-use">mTLS service mesh</div></div>
  <div class="tool"><div class="tool-name">Keycloak</div><div class="tool-use">OAuth2 + RBAC + MFA</div></div>
  <div class="tool"><div class="tool-name">HashiCorp Vault</div><div class="tool-use">Secrets management</div></div>
  <div class="tool"><div class="tool-name">Prometheus</div><div class="tool-use">Metrics collection</div></div>
  <div class="tool"><div class="tool-name">Grafana</div><div class="tool-use">Observability dashboards</div></div>
  <div class="tool"><div class="tool-name">Loki</div><div class="tool-use">Log aggregation</div></div>
  <div class="tool"><div class="tool-name">Falco</div><div class="tool-use">Runtime security</div></div>
  <div class="tool"><div class="tool-name">Kyverno</div><div class="tool-use">Kubernetes policies</div></div>
  <div class="tool"><div class="tool-name">Semgrep</div><div class="tool-use">SAST code scanning</div></div>
  <div class="tool"><div class="tool-name">Trivy</div><div class="tool-use">Container + IaC scanning</div></div>
  <div class="tool"><div class="tool-name">OWASP ZAP</div><div class="tool-use">DAST runtime scanning</div></div>
  <div class="tool"><div class="tool-name">Flagsmith</div><div class="tool-use">Feature flags</div></div>
  <div class="tool"><div class="tool-name">Grafana OnCall</div><div class="tool-use">Incident paging</div></div>
  <div class="tool"><div class="tool-name">Velero</div><div class="tool-use">Cluster backup + restore</div></div>
  <div class="tool"><div class="tool-name">MinIO</div><div class="tool-use">S3-compatible object store</div></div>
  <div class="tool"><div class="tool-name">RabbitMQ</div><div class="tool-use">Message broker</div></div>
  <div class="tool"><div class="tool-name">pgvector</div><div class="tool-use">Postgres vector search</div></div>
  <div class="tool"><div class="tool-name">Cosign</div><div class="tool-use">Container image signing</div></div>
  <div class="tool"><div class="tool-name">Ansible</div><div class="tool-use">Node bootstrap + config</div></div>
</div>

<h2>Infrastructure Agnostic</h2>
<div class="note">Citadel runs on <strong>any Linux host with SSH + Docker</strong>: VPS, bare metal, on-prem, edge devices, home lab, any cloud. No vendor lock-in, no proprietary APIs. The infrastructure layer is Terraform modules targeting a generic <code>ssh://user@host</code> provider.</div>

<footer>
  <div>Citadel Cloud Management &#x00B7; MIT License &#x00B7; 2026</div>
  <div>Generated from <code>.claude/agents/_registry.yaml</code></div>
</footer>

</div>
</body>
</html>
"""


def main() -> int:
    out = render()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(out, encoding="utf-8", newline="\n")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(out):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
