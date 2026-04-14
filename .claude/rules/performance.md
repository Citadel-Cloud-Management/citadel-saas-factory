# Performance Rules
- Cache strategy: Redis for hot data, CDN for static assets
- Lazy loading for frontend routes and heavy components
- Pagination on all list queries (no unbounded selects)
- Query optimization: no N+1, use JOINs and eager loading
- Connection pooling for database and Redis
- Bundle analysis and code splitting for frontend
