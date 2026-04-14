# Architecture

System architecture for Citadel SaaS Factory.

## High-Level Overview

Citadel SaaS Factory follows **clean architecture** principles with strict dependency direction: outer layers depend on inner layers, never the reverse.

```
+-------------------------------------------------------+
|                    Infrastructure                      |
|  (Docker, K3s, ArgoCD, Traefik, Vault, MinIO)         |
|                                                        |
|  +--------------------------------------------------+ |
|  |                  Interfaces                       | |
|  |  (API Routes, WebSocket, CLI, Event Handlers)     | |
|  |                                                    | |
|  |  +----------------------------------------------+ | |
|  |  |              Use Cases                       | | |
|  |  |  (Application Services, Agent Orchestration) | | |
|  |  |                                              | | |
|  |  |  +----------------------------------------+  | | |
|  |  |  |            Domain                      |  | | |
|  |  |  |  (Entities, Value Objects, Interfaces) |  | | |
|  |  |  +----------------------------------------+  | | |
|  |  +----------------------------------------------+ | |
|  +--------------------------------------------------+ |
+-------------------------------------------------------+
```

## Layer Details

### Domain Layer (Innermost)

The domain layer contains business logic with zero external dependencies.

- **Entities**: Core business objects (Tenant, User, Subscription, Agent)
- **Value Objects**: Immutable typed values (Email, Money, AgentId)
- **Domain Interfaces**: Abstract repository and service contracts
- **Domain Events**: Business events (TenantCreated, SubscriptionUpgraded)

### Use Case Layer

Application-specific business rules that orchestrate domain entities.

- **Application Services**: Coordinate domain objects to fulfill use cases
- **Agent Orchestration**: Manage the 265-agent lifecycle and execution
- **DTOs**: Data transfer objects for layer boundary crossing
- **Ports**: Input/output port interfaces (dependency inversion)

### Interface Layer

Adapters that translate between external protocols and use cases.

- **API Routes**: FastAPI endpoints (RESTful, versioned under `/api/v1/`)
- **WebSocket Handlers**: Real-time communication for agent status
- **CLI Commands**: Administrative and development tooling
- **Event Handlers**: RabbitMQ consumers for async processing

### Infrastructure Layer (Outermost)

Concrete implementations of domain and use case interfaces.

- **PostgreSQL Repositories**: SQLAlchemy-backed data access
- **Redis Cache**: Hot data caching with TTL management
- **MinIO Storage**: S3-compatible object storage adapter
- **Keycloak Auth**: OAuth2/OIDC authentication and RBAC
- **RabbitMQ Messaging**: Async event publishing and consuming

## Backend Architecture (FastAPI)

```
backend/
  app/
    domain/           # Entities, value objects, interfaces
    use_cases/        # Application services
    api/
      v1/             # Versioned REST endpoints
      deps.py         # Dependency injection
    infrastructure/
      db/             # SQLAlchemy models, migrations (Alembic)
      cache/          # Redis client and cache strategies
      storage/        # MinIO/S3 adapter
      auth/           # Keycloak integration
      messaging/      # RabbitMQ publisher/consumer
    core/
      config.py       # Settings (Pydantic BaseSettings)
      security.py     # JWT, CORS, rate limiting
```

### Dependency Injection

FastAPI's dependency injection system wires infrastructure to use cases at runtime:

```python
# deps.py
def get_user_repository() -> UserRepository:
    return PostgresUserRepository(get_db_session())

def get_user_service(
    repo: UserRepository = Depends(get_user_repository),
    cache: CacheService = Depends(get_cache_service),
) -> UserService:
    return UserService(repo=repo, cache=cache)
```

Use cases never import infrastructure directly. They depend on abstract interfaces defined in the domain layer, with concrete implementations injected at the interface layer.

## Frontend Architecture (Next.js 14)

```
frontend/
  src/
    app/              # App Router (pages, layouts, loading states)
    components/
      ui/             # Design system primitives (Button, Input, Card)
      features/       # Feature-specific components (Dashboard, AgentPanel)
    hooks/            # Custom React hooks
    lib/
      api/            # API client (typed fetch wrappers)
      auth/           # Keycloak OIDC integration
      store/          # Zustand state management
    types/            # Shared TypeScript types
```

### State Management

- **Server State**: React Server Components + fetch with revalidation
- **Client State**: Zustand stores (no prop drilling)
- **Form State**: React Hook Form + Zod validation
- **Cache**: SWR or React Query for client-side API caching

## Infrastructure Architecture

### Service Mesh (Linkerd)

All service-to-service communication is encrypted via **mTLS** through Linkerd:

```
Service A  -->  Linkerd Proxy  -->  Linkerd Proxy  -->  Service B
               (encrypt)            (decrypt)
```

Benefits:

- Automatic mTLS without application changes
- Observability (golden metrics per route)
- Retries and timeouts at the mesh level
- Traffic splitting for canary deployments

### Orchestration (K3s + ArgoCD)

```
Git Repository (source of truth)
       |
       v
   ArgoCD (watches git, syncs to cluster)
       |
       v
   K3s Cluster
     +-- Namespace: production
     +-- Namespace: staging
     +-- Namespace: monitoring
     +-- Namespace: security
```

ArgoCD enforces **GitOps**: the desired state is always in git. Manual `kubectl apply` is never used in production.

### Reverse Proxy (Traefik)

Traefik handles ingress routing, TLS termination, and middleware:

- Automatic Let's Encrypt certificates
- Rate limiting middleware
- CORS headers
- Request/response compression
- Circuit breaker for upstream failures

## Data Flow

### Request Lifecycle

```
Client Request
  --> Traefik (TLS termination, rate limit, routing)
    --> Linkerd Proxy (mTLS encryption)
      --> FastAPI (authentication, authorization)
        --> Use Case (business logic)
          --> Repository (data access)
            --> PostgreSQL / Redis / MinIO
          <-- Response DTO
        <-- API Response Envelope { data, error, meta }
      <-- Linkerd Proxy
    <-- Traefik
  <-- Client Response
```

### Event-Driven Flow

```
API Handler (publishes event)
  --> RabbitMQ Exchange
    --> Queue: agent-tasks
      --> Agent Worker (consumes, processes)
        --> Repository (persist results)
        --> RabbitMQ (publish completion event)
    --> Queue: notifications
      --> Notification Worker (email, webhook, Slack)
    --> Queue: analytics
      --> Analytics Worker (metrics, dashboards)
```

## Multi-Tenancy

- **Database**: Row-Level Security (RLS) in PostgreSQL isolates tenant data
- **Auth**: Keycloak realms or tenant-scoped roles
- **Storage**: MinIO bucket-per-tenant isolation
- **Cache**: Redis key prefix per tenant (`tenant:{id}:key`)

## Technology Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| API Gateway | Traefik | Ingress, TLS, rate limiting |
| Service Mesh | Linkerd | mTLS, observability |
| Backend | FastAPI | REST API, business logic |
| Frontend | Next.js 14 | UI, SSR, static assets |
| Database | PostgreSQL 16 | Persistent storage, RLS |
| Cache | Redis 7 | Session, hot data, pub/sub |
| Auth | Keycloak 24 | OAuth2, RBAC, MFA |
| Storage | MinIO | S3-compatible objects |
| Messaging | RabbitMQ | Async events, task queues |
| Orchestration | K3s + ArgoCD | GitOps deployment |
| Secrets | HashiCorp Vault | Secret management |
| Monitoring | Prometheus + Grafana | Metrics, dashboards |
| Logging | Loki | Log aggregation |
| Security | Falco + Kyverno | Runtime + policy enforcement |
