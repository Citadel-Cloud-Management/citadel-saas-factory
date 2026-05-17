# Scripts

Automation scripts for bootstrapping, deployment, and maintenance.

## Setup & Bootstrap

| Script | Purpose |
|--------|---------|
| `setup.sh` | Verify agentic infrastructure (15-point check) |
| `bootstrap.sh` | Install all dependencies |
| `parallel-bootstrap.sh` | Parallel dependency installation |
| `verify-install.sh` | Post-install verification |
| `setup-tokens.sh` | Interactive API key configuration |

## Deployment

| Script | Purpose |
|--------|---------|
| `deploy.sh` | Build, push, and deploy to K8s |
| `rollback.sh` | Emergency rollback via ArgoCD |

## Configuration

| Script | Purpose |
|--------|---------|
| `install-hooks.sh` | Set up git pre-commit hooks |
| `install-mcp.sh` | Configure MCP servers |
| `install-models.sh` | Set up model providers |
| `setup-guardrails.sh` | Initialize guardrails validation |
| `switch-engine.sh` | Switch between model engines (paid/free/local) |
| `detect-business.sh` | Detect business domain for agent configuration |

## Knowledge Management

| Script | Purpose |
|--------|---------|
| `generate-vault.py` | Generate Obsidian vault structure |
| `sync-vault-memory.py` | Sync .claude/memory to vault |
| `vault-autolink.py` | Generate Obsidian backlinks |
| `render-agents.sh` | Render agent definitions |
| `generate-strategy-html.py` | Generate strategy visualization |
