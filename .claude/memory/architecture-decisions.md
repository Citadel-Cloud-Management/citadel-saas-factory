# Architecture Decisions

## ADR-001: Infrastructure Agnostic
- No cloud vendor lock-in. Runs on any Linux server with SSH + Docker.
- Open-source alternatives: MinIO (S3), Keycloak (Cognito), Vault (KMS).

## ADR-002: Free Toolchain ($0/month)
- K3s, Traefik, Linkerd, Keycloak, Vault, Prometheus, Grafana, Loki, Falco, Kyverno, Semgrep, Trivy.

## ADR-003: 265-Agent Architecture
- 15 business domains, each agent focused single-responsibility.
- Registry-defined in .claude/agents/_registry.yaml, 11 with full definitions.

## ADR-004: GitOps (ArgoCD + Kustomize)
- Declarative, auditable, self-healing deployments via gitops/ overlays.

## ADR-005: Multi-Model Routing
- 12 providers, 8 tiers. Agents reference tiers, not specific models.
- Swap providers by changing one env var. See models/routing.yaml.

## ADR-006: Harness-First Architecture
- 98.4% deterministic infrastructure, 1.6% AI decision logic (VILA-Lab research).
- Hooks > CLAUDE.md for enforcement. Permissions deny-first.

## ADR-007: DeerFlow as External Dependency
- Removed embedded 1,099-file fork. Now clone separately or use as git submodule.
- Integration guide: docs/references/deer-flow.md.

## ADR-008: CLAUDE.md Under 200 Lines
- Uses @imports to .claude/rules/ for detailed conventions.
- Keeps context window lean for better model adherence.

## ADR-009: Cross-IDE Support
- 10+ AI platforms configured: Claude, Cursor, Codex, Jules, Devin, Factory, Antigravity, Windsurf, Continue, Daytona, Codegen.
- AGENTS.md for universal instructions, platform-specific configs in dot-directories.
