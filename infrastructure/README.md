# Infrastructure

Infrastructure-as-code for deploying the Citadel SaaS Factory. Runs on any Linux server with SSH and Docker.

## Components

| Directory | Tool | Purpose |
|-----------|------|---------|
| `terraform/` | Terraform | Server provisioning, networking, K8s bootstrap |
| `helm/` | Helm | Kubernetes application charts |
| `ansible/` | Ansible | Configuration management playbooks |
| `mesh/` | Linkerd | Service mesh (mTLS, traffic policies) |
| `agent-protocols/` | Custom | Inter-agent communication (MCP, A2A, ACP) |

## Terraform Modules

```
terraform/
├── modules/
│   ├── compute/        Server provisioning
│   ├── network/        VPC, subnets, security groups
│   ├── k8s-bootstrap/  K3s cluster initialization
│   ├── server/         Base server configuration
│   └── platform-stack/ Full platform deployment
└── environments/
    ├── staging/
    └── production/
```

## Agent Communication Protocols

| Protocol | Owner | Use Case |
|----------|-------|----------|
| MCP | Anthropic | Tool invocation for LLM agents |
| A2A | Google | Agent-to-Agent communication |
| ACP | IBM | Agent Communication Protocol |

## Deploy

```bash
cd infrastructure/terraform/environments/staging
terraform init && terraform plan && terraform apply
```
