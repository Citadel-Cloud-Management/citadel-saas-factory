# Architecture Rules
- Clean architecture: domain > use cases > interfaces > infrastructure
- Dependency direction: outer layers depend on inner layers, never reverse
- Domain-driven design: ubiquitous language, bounded contexts
- Repository pattern for data access
- Service layer for business logic
- No business logic in controllers or routes
