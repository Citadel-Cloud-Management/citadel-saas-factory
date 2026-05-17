# MCP — Model Context Protocol Servers

43 MCP server configurations for connecting agents to external tools.

## What is MCP?

The [Model Context Protocol](https://modelcontextprotocol.io) is an open standard for connecting AI tools to external data sources. MCP servers give agents access to databases, APIs, issue trackers, and more.

## Registry

`registry.yaml` contains 43 server configurations across categories:

| Category | Servers |
|----------|---------|
| Core | filesystem, fetch, memory, sequential-thinking |
| Version Control | github, gitlab |
| Search | brave-search, exa, tavily |
| Database | postgres, mongodb, redis, supabase |
| Vector | chroma, pinecone, qdrant, weaviate |
| Monitoring | prometheus, grafana, datadog, sentry |
| Communication | slack, discord, gmail |
| Design | figma |
| Project Management | jira, asana, linear, notion |
| AI/ML | anthropic, openai, ollama, huggingface |
| Infrastructure | docker, kubernetes, cloudflare, aws |

## Configure

```bash
claude mcp add github npx -y @modelcontextprotocol/server-github
claude mcp add postgres npx -y @modelcontextprotocol/server-postgres
claude mcp list
```

## Project MCP Configs

`.claude/mcp/` contains 8 pre-configured servers: docker, filesystem, github, kubernetes, postgres, prometheus, redis, vault.
