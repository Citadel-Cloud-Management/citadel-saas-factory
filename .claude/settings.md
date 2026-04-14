# Hook Documentation

## PreToolUse Hooks

### Python Linting
- **Matcher**: `Write(*.py)`
- **Action**: Runs `ruff check` on the file before writing
- **Timeout**: 10 seconds
- **Purpose**: Catches linting errors before they're committed

### TypeScript/React Linting
- **Matcher**: `Write(*.ts)|Write(*.tsx)`
- **Action**: Runs `eslint` on the file before writing
- **Timeout**: 10 seconds
- **Purpose**: Enforces code standards on frontend files

## PostToolUse Hooks

### Python Auto-Format
- **Matcher**: `Write(*.py)`
- **Action**: Runs `ruff format` on the file after writing
- **Purpose**: Ensures consistent Python formatting

### TypeScript/React Auto-Format
- **Matcher**: `Write(*.ts)|Write(*.tsx)`
- **Action**: Runs `prettier --write` on the file after writing
- **Purpose**: Ensures consistent frontend formatting

## Permissions

### Allowed
- Read, Write, Edit (general file operations)
- Git commands (`git *`)
- npm commands (`npm *`)
- Make commands (`make *`)
- Docker commands (`docker *`)

### Denied
- Reading `.env` files (secret protection)
- Writing to production config files
