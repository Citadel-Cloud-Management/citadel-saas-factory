# Error Patterns

Known issues and resolutions. Updated by agents during development.

## Hook Misconfiguration
- **Trigger**: `if: "Bash(rm -rf *)"` in PreToolUse hook blocks ALL Bash commands
- **Fix**: Remove redundant hook; use `permissions.deny` rules instead for command blocking
- **Prevention**: Test hooks with `--debug` flag; `if` patterns match broadly

## Vault Stub Bloat
- **Trigger**: Auto-generating one vault note per registry agent (265 stubs)
- **Fix**: Removed stubs; registry is source of truth for agent metadata
- **Prevention**: Only create vault notes with real knowledge content, not boilerplate

## Embedded Fork Bloat
- **Trigger**: Copying full third-party project (DeerFlow, 1,099 files) into repo
- **Fix**: `git rm -r deer-flow/`, added to .gitignore, created integration guide
- **Prevention**: Use git submodules or document as external dependency

## CLAUDE.md Instruction Loss
- **Trigger**: CLAUDE.md exceeds 200 lines; model ignores rules buried in long files
- **Fix**: Refactored from 269 to 112 lines using @imports for .claude/rules/
- **Prevention**: Prune test: "Would removing this cause mistakes?" If no, delete it.

## Template
```
### [ERROR_CODE] Short description
- Trigger: What causes it
- Fix: How to resolve
- Prevention: How to avoid
```
