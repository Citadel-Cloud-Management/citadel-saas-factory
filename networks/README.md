# Networks

Network configurations for the Citadel SaaS Factory multi-agent system.

## Layers

| Layer | Directory | Purpose |
|-------|-----------|---------|
| Agent Mesh | `mesh/` | Multi-agent coordination (Ruflo, CrewAI, LangGraph) |
| Service Mesh | `service-mesh/` | mTLS, traffic management (Linkerd, Istio) |
| Container | `container/` | CNI and network policies (Cilium, Calico) |
| VPN/Overlay | `vpn/` | Zero-trust access (Tailscale, WireGuard) |
| Discovery | `discovery/` | Service discovery (Consul, CoreDNS) |
| Agent Protocols | `agent-protocols/` | Inter-agent communication (MCP, A2A, ACP) |

## Agent Communication Protocols

| Protocol | Owner | Use Case |
|----------|-------|----------|
| MCP | Anthropic | Tool invocation for LLM agents |
| A2A | Google | Agent-to-Agent communication |
| ACP | IBM | Agent Communication Protocol |
| AGNTCY | Open | Open agent network standard |
| AutoGen | Microsoft | Multi-agent orchestration |

## Configuration

Each directory contains YAML configs with sensible defaults. Override via environment variables or by editing the configs directly.
