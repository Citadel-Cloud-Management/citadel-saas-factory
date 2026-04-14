# ADR-002: PostgreSQL with pgvector as Primary Database

## Status

Accepted

## Context

Citadel SaaS Factory requires a database that supports:

- Multi-tenant data isolation with row-level security
- ACID transactions for financial operations (billing, subscriptions)
- Vector similarity search for AI agent embeddings and semantic search
- Mature ecosystem with strong tooling, backup, and replication support
- Zero licensing cost (aligned with the $0/month software cost target)

The primary candidates evaluated were PostgreSQL, MySQL, and MongoDB.

## Decision

We chose **PostgreSQL 16 with the pgvector extension** as the primary database.

### Key Reasons

1. **ACID compliance**: PostgreSQL provides full ACID transaction support, essential for financial operations (Stripe billing, subscription management) and multi-step agent state persistence.

2. **Row-Level Security (RLS)**: Native RLS policies enable multi-tenant data isolation at the database level. Each query is automatically filtered by tenant ID, preventing data leakage without application-level enforcement.

   ```sql
   CREATE POLICY tenant_isolation ON orders
     USING (tenant_id = current_setting('app.current_tenant')::uuid);
   ```

3. **pgvector for vector search**: The pgvector extension adds vector similarity search directly in PostgreSQL, eliminating the need for a separate vector database (Pinecone, Weaviate). This simplifies infrastructure while supporting AI agent embeddings.

   ```sql
   CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops);
   SELECT * FROM embeddings ORDER BY embedding <=> $1 LIMIT 10;
   ```

4. **Mature ecosystem**: PostgreSQL has decades of production use, extensive documentation, and robust tooling for backup (pg_dump, WAL archiving), replication (streaming, logical), and monitoring (pg_stat_statements).

5. **Zero cost**: PostgreSQL is fully open source (PostgreSQL License), with no per-node, per-core, or enterprise licensing fees.

## Consequences

### Positive

- Single database handles relational data and vector search (reduced infrastructure)
- RLS provides defense-in-depth for multi-tenant isolation
- Strong transaction support prevents data corruption in financial flows
- Extensive indexing options (B-tree, GiST, GIN, BRIN, IVFFlat) for query optimization
- Well-supported by SQLAlchemy, Alembic, and the Python ecosystem

### Negative

- Horizontal scaling requires more effort than MongoDB (no native sharding)
- pgvector performance may not match dedicated vector databases at very large scale (100M+ vectors)
- RLS policies add complexity to query planning and debugging
- Requires careful connection pool management under high concurrency

### Mitigations

- Use connection pooling (PgBouncer or SQLAlchemy pool) to manage connections efficiently
- Monitor query performance with `pg_stat_statements` and `EXPLAIN ANALYZE`
- If vector search scale exceeds pgvector limits, migrate to a dedicated vector database while keeping relational data in PostgreSQL
- Use read replicas to distribute query load for analytics workloads
