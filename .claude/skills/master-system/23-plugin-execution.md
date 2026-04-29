---
name: ms-plugin-execution
description: Claude Code plugin execution rules — inspect repo structure first, analyze dependencies, identify build systems, validate environment requirements, map infrastructure dependencies. Safety checks before code changes and deployments.
type: directive
priority: 23
---

# Claude Code Plugin Execution Rules

## Core Rule

When operating with Claude Code plugins, follow a disciplined execution protocol. Understand before acting.

## Before Any Work — Repository Assessment

### Always Do First
```
1. Inspect repository structure (Glob/LS at root)
2. Analyze dependencies (package.json, pyproject.toml, go.mod, Cargo.toml)
3. Identify build systems (Makefile, scripts/, CI configs)
4. Validate environment requirements (.env.example, docker-compose.yml)
5. Identify secrets/config dependencies (vault refs, secret stores)
6. Map infrastructure dependencies (terraform/, helm/, k8s manifests)
7. Check existing tests (test patterns, coverage config)
8. Read CLAUDE.md and project conventions
```

### Assessment Output
```yaml
repository:
  language: <primary language>
  framework: <primary framework>
  build_system: <make/npm/gradle/cargo>
  test_framework: <pytest/vitest/go test>
  ci_system: <github-actions/gitlab-ci/jenkins>
  infrastructure: <terraform/helm/raw-k8s>
  secrets_management: <vault/env/cloud-kms>
  deployment: <argocd/flux/manual>
```

## Before Changing Code

### Impact Assessment
```
[ ] What files will be modified?
[ ] What systems are affected by this change?
[ ] Are there security implications?
[ ] Is there a rollback path?
[ ] Will existing tests still pass?
[ ] Are there database migration requirements?
[ ] Does this require infrastructure changes?
[ ] Are environment variables needed?
```

### Change Classification
| Type | Risk | Requires |
|------|------|----------|
| Bug fix (isolated) | Low | Tests pass |
| New feature (additive) | Medium | Tests + review |
| Refactor (structural) | Medium-High | Full test suite |
| Schema migration | High | Backup + rollback plan |
| Auth/security change | Critical | Security review |
| Infrastructure change | Critical | Plan + approval |

## Before Deployment

### Pre-Deployment Checklist
```
[ ] All tests pass (unit, integration, E2E)
[ ] Infrastructure validated (terraform plan)
[ ] Secrets verified (available in target environment)
[ ] Dependencies scanned (no critical CVEs)
[ ] IAM implications reviewed (no privilege escalation)
[ ] Rollback procedure documented
[ ] Monitoring alerts configured
[ ] Runbook updated if needed
```

### Deployment Safety Protocol
```
1. Verify current state is healthy
2. Create deployment record
3. Deploy to staging first
4. Run smoke tests on staging
5. Wait for approval gate
6. Deploy to production (canary)
7. Monitor error rates for 10 minutes
8. Promote to full deployment or rollback
9. Verify production health
10. Close deployment record
```

## Tool Usage Discipline

### Prefer Dedicated Tools
| Task | Use This | Not This |
|------|----------|----------|
| Read files | Read tool | cat/head/tail in Bash |
| Search files | Glob tool | find in Bash |
| Search content | Grep tool | grep/rg in Bash |
| Edit files | Edit tool | sed/awk in Bash |
| Create files | Write tool | echo/cat heredoc in Bash |

### Bash Reserved For
- Git operations
- Build commands (make, npm run, cargo)
- Docker/kubectl commands
- Running test suites
- System commands (env, process management)

## Error Recovery

If a plugin operation fails:
1. Read the error message carefully
2. Check if it's a permission issue
3. Verify prerequisites are met
4. Try a more targeted approach
5. If stuck after 3 attempts, explain the issue to the user
