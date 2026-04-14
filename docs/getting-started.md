# Getting Started

Step-by-step guide to set up Citadel SaaS Factory from scratch.

## Prerequisites

Before you begin, ensure you have the following installed:

| Tool | Minimum Version | Purpose |
|------|----------------|---------|
| Node.js | 18+ | Frontend build, Claude Code CLI |
| Python | 3.12+ | Backend (FastAPI) |
| Docker | 24+ | Container runtime |
| Docker Compose | 2.20+ | Local orchestration |
| Git | 2.40+ | Version control |
| GitHub CLI (`gh`) | 2.40+ | GitHub operations |

### API Keys Required

- **ANTHROPIC_API_KEY** -- Claude API access for agent system
- **GITHUB_PERSONAL_ACCESS_TOKEN** -- GitHub API access for automation

## 1. Clone the Repository

```bash
git clone https://github.com/kogunlowo123/citadel-saas-factory.git
cd citadel-saas-factory
```

## 2. Configure Tokens

Run the interactive setup script:

```bash
chmod +x scripts/setup-tokens.sh
./scripts/setup-tokens.sh
```

This will prompt you for your API keys, write them to `~/.bashrc`, and authenticate the GitHub CLI.

Alternatively, configure manually:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
echo 'export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_..."' >> ~/.bashrc
source ~/.bashrc

gh auth login --with-token <<< "$GITHUB_PERSONAL_ACCESS_TOKEN"
```

## 3. Bootstrap the Project

Run the bootstrap script to install all dependencies and initialize services:

```bash
chmod +x scripts/bootstrap.sh
./scripts/bootstrap.sh
```

This script will:

- Install Python dependencies (`poetry install` or `pip install -r requirements.txt`)
- Install Node.js dependencies (`npm ci`)
- Pull required Docker images
- Initialize the database schema
- Seed default configuration

## 4. Verify Installation

Run the verification script to confirm everything is correctly configured:

```bash
chmod +x scripts/verify-install.sh
./scripts/verify-install.sh
```

You should see 10/10 checks passing. Fix any failures using the suggestions provided.

## 5. First Run (Local Development)

Start all services locally with Docker Compose:

```bash
docker-compose up -d
```

Services will be available at:

| Service | URL |
|---------|-----|
| Frontend (Next.js) | http://localhost:3000 |
| Backend API (FastAPI) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| Keycloak (Auth) | http://localhost:8080 |
| MinIO Console | http://localhost:9001 |
| Grafana (Monitoring) | http://localhost:3001 |
| RabbitMQ Management | http://localhost:15672 |

### Verify Services Are Running

```bash
# Check all containers are healthy
docker-compose ps

# Test API health endpoint
curl http://localhost:8000/health

# Test frontend
curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
```

## 6. Run the Agent System

With `CYCLE_INTERVAL=0`, agents run on-demand rather than on a polling loop:

```bash
# Run a single agent
python -m agents.run --agent ceo-strategist

# Run all agents in a domain
python -m agents.run --domain marketing

# Check agent registry
python -m agents.registry --list
```

## Next Steps

- [Architecture Overview](architecture.md) -- Understand the system design
- [Agent System](agents.md) -- Learn how the 265 agents work
- [Deployment Guide](deployment.md) -- Deploy to staging and production
- [Security Guide](security.md) -- Harden your deployment
