# 8-Layer AI Memory Architecture

> Production-grade memory system for stateful, persistent, context-aware AI in SaaS applications.
> Implementation: `backbone/memory/`

---

## 1. System Architecture

```
                              ┌─────────────────────────────┐
                              │     LLM Provider (Claude,    │
                              │     GPT, Gemini, Local)      │
                              └─────────────┬───────────────┘
                                            │
                              ┌─────────────▼───────────────┐
                              │    MEMORY ORCHESTRATOR       │
                              │   backbone/memory/           │
                              │   orchestrator.py            │
                              │                              │
                              │  PRE-INFERENCE:              │
                              │   Assemble context from      │
                              │   all 8 layers               │
                              │                              │
                              │  POST-INFERENCE:             │
                              │   Write back learnings,      │
                              │   episodes, updates          │
                              └──┬──┬──┬──┬──┬──┬──┬──┬─────┘
                                 │  │  │  │  │  │  │  │
        ┌────────────────────────┘  │  │  │  │  │  │  └──────────────────────┐
        │                    ┌──────┘  │  │  │  │  └──────────┐              │
        ▼                    ▼         ▼  │  ▼  │             ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────┴──┐ ┌┴───────┐ ┌──────────┐ ┌──────────┐
│ L1: WORKING  │ │ L2: SHORT    │ │ L3: LONG│ │L4: EPIS│ │L5: SEMAN │ │L6: PROCED│
│   MEMORY     │ │   TERM       │ │  TERM   │ │  ODIC  │ │  TIC     │ │  URAL    │
│              │ │              │ │         │ │        │ │          │ │          │
│ In-process   │ │ Redis        │ │ Postgres│ │Postgres│ │ pgvector │ │ Postgres │
│ token budget │ │ session buf  │ │ RLS     │ │partitnd│ │ HNSW idx │ │ workflow │
└──────────────┘ └──────────────┘ └─────────┘ └────────┘ └──────────┘ └──────────┘
                                                                ┌──────────┐ ┌──────────┐
                                                                │L7: ENTITY│ │L8: SHARED│
                                                                │          │ │          │
                                                                │ Postgres │ │ Redis    │
                                                                │ + Neo4j  │ │ pub/sub  │
                                                                └──────────┘ └──────────┘
```

### Data Flow

```
User Request
    │
    ▼
┌─ PRE-INFERENCE ────────────────────────────────────────────────────────────────┐
│  1. Working Memory: load system prompt, allocate token budget                  │
│  2. Entity Memory:  load user profile, inject as system context                │
│  3. Long-Term:      query user preferences, facts, corrections                 │
│  4. Semantic:       RAG retrieval — embed query, search, rerank                │
│  5. Procedural:     find applicable workflows for this context                 │
│  6. Episodic:       load relevant past interactions                            │
│  7. Shared:         load multi-agent coordination state                        │
│  8. Short-Term:     load recent conversation turns                             │
│  9. Working Memory: truncate all injections to fit context window              │
└────────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─ INFERENCE ────────────────────────────────────────────────────────────────────┐
│  Send assembled context → LLM → Receive response                               │
│  Guardrails validation (hallucination, PII, toxicity)                          │
└────────────────────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─ POST-INFERENCE ───────────────────────────────────────────────────────────────┐
│  1. Short-Term:  append user message + assistant response                      │
│  2. Episodic:    record conversation episode with timestamp                    │
│  3. Long-Term:   extract and store any new facts learned                       │
│  4. Entity:      update interaction count, last_seen, new attributes           │
│  5. Procedural:  if workflow completed, update success stats                   │
│  6. Shared:      if multi-agent, broadcast state update                        │
└────────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tech Stack

| Layer | Storage | Latency | Cost | Scalability |
|-------|---------|---------|------|-------------|
| L1: Working | In-process | <1ms | $0 (memory only) | Per-instance |
| L2: Short-Term | Redis 7 | 1-5ms | ~$15/mo (ElastiCache t3.small) | Cluster mode |
| L3: Long-Term | PostgreSQL 16 + RLS | 5-20ms | ~$30/mo (RDS t3.small) | Read replicas |
| L4: Episodic | PostgreSQL 16 (partitioned) | 5-20ms | ~$30/mo (shared with L3) | Time partitions |
| L5: Semantic | pgvector (HNSW) | 10-50ms | ~$50/mo (RDS with pgvector) | IVFFlat/HNSW |
| L6: Procedural | PostgreSQL 16 | 5-20ms | ~$0 (shared with L3) | Same instance |
| L7: Entity | PostgreSQL 16 + Neo4j (optional) | 5-50ms | ~$0-100/mo | Graph sharding |
| L8: Shared | Redis 7 (pub/sub) | 1-5ms | ~$0 (shared with L2) | Redis Cluster |

**Total baseline: ~$95/mo** for a production-ready 8-layer system using shared PostgreSQL + Redis.

### Trade-offs

| Decision | Chosen | Alternative | Why |
|----------|--------|-------------|-----|
| Vector DB | pgvector | Qdrant, Pinecone | Zero new infra; same Postgres instance; HNSW is fast enough to 10M vectors |
| STM + Shared | Redis | DynamoDB, Memcached | Sub-ms latency, pub/sub built in, TTL native |
| Episodic partitioning | Monthly partitions | TimescaleDB | Standard Postgres; no extension dependency for time-series |
| Entity graph | Postgres + optional Neo4j | Neptune, ArangoDB | Start relational; add graph overlay only when relationship queries dominate |
| Embedding model | text-embedding-3-small | Cohere embed, BGE | Best price/performance; 1536 dims; OpenAI-compatible API |
| Reranker | Cohere Rerank v3 | Cross-encoder, ColBERT | 10x retrieval quality uplift; <100ms latency; pay-per-query |

---

## 3. Data Design

### 3.1 Entity Memory (Relational + Graph)

```sql
-- Core entity table
CREATE TABLE entity_profiles (
    entity_id          TEXT PRIMARY KEY,
    tenant_id          TEXT NOT NULL,
    entity_type        TEXT NOT NULL,  -- user | organization | product | agent | service
    name               TEXT NOT NULL,
    attributes         JSONB DEFAULT '{}',
    preferences        JSONB DEFAULT '{}',
    history_summary    TEXT DEFAULT '',
    first_seen_at      TIMESTAMPTZ DEFAULT now(),
    last_seen_at       TIMESTAMPTZ DEFAULT now(),
    interaction_count  INTEGER DEFAULT 0,
    tags               TEXT[] DEFAULT '{}'
);

-- Relationship edges
CREATE TABLE entity_relationships (
    id          SERIAL PRIMARY KEY,
    tenant_id   TEXT NOT NULL,
    from_id     TEXT NOT NULL REFERENCES entity_profiles(entity_id),
    to_id       TEXT NOT NULL REFERENCES entity_profiles(entity_id),
    relation    TEXT NOT NULL,  -- belongs_to | manages | uses | created_by
    created_at  TIMESTAMPTZ DEFAULT now(),
    UNIQUE(tenant_id, from_id, to_id, relation)
);
```

### 3.2 Episodic Memory (Event-Based)

```sql
CREATE TABLE episodic_memory (
    entry_id      TEXT PRIMARY KEY,
    tenant_id     TEXT NOT NULL,
    user_id       TEXT NOT NULL,
    session_id    TEXT NOT NULL,
    kind          TEXT NOT NULL,  -- conversation | tool_call | error | deployment | decision | feedback
    summary       TEXT NOT NULL,
    detail        JSONB DEFAULT '{}',
    actors        TEXT[] DEFAULT '{}',
    outcome       TEXT DEFAULT '',
    duration_ms   INTEGER DEFAULT 0,
    created_at    TIMESTAMPTZ DEFAULT now(),
    embedding_id  TEXT DEFAULT '',
    tags          TEXT[] DEFAULT '{}'
) PARTITION BY RANGE (created_at);
```

### 3.3 Long-Term Memory (User Profiles)

```sql
CREATE TABLE long_term_memory (
    entry_id     TEXT PRIMARY KEY,
    tenant_id    TEXT NOT NULL,
    user_id      TEXT NOT NULL,
    namespace    TEXT NOT NULL DEFAULT 'general',  -- preferences | facts | corrections | feedback
    key          TEXT NOT NULL,
    value        JSONB NOT NULL,
    confidence   REAL DEFAULT 1.0,
    source       TEXT DEFAULT '',
    created_at   TIMESTAMPTZ DEFAULT now(),
    updated_at   TIMESTAMPTZ DEFAULT now(),
    access_count INTEGER DEFAULT 0,
    tags         TEXT[] DEFAULT '{}',
    UNIQUE(tenant_id, user_id, key)
);
```

### 3.4 Vector DB Indexing Strategy

```sql
-- pgvector HNSW index (fast approximate nearest neighbor)
CREATE INDEX idx_sem_embedding ON semantic_chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Full-text search for hybrid retrieval
ALTER TABLE semantic_chunks ADD COLUMN fts tsvector
    GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;
CREATE INDEX idx_sem_fts ON semantic_chunks USING GIN(fts);

-- Hybrid query: 70% vector + 30% keyword
SELECT *,
    0.7 * (1 - (embedding <=> query_vec)) +
    0.3 * ts_rank(fts, plainto_tsquery('english', query_text)) AS score
FROM semantic_chunks
WHERE tenant_id = $1
ORDER BY score DESC LIMIT 10;
```

---

## 4. Implementation Plan

### Phase 1: MVP (Week 1-2)

| Step | What | Files |
|------|------|-------|
| 1 | Deploy schemas via Alembic migrations | `backend/alembic/versions/` |
| 2 | Wire Working + Short-Term memory | `working_memory.py`, `short_term_memory.py` |
| 3 | Wire Long-Term + Entity memory | `long_term_memory.py`, `entity_memory.py` |
| 4 | Wire Orchestrator with 4 active layers | `orchestrator.py` |
| 5 | Mount API routes on FastAPI | `api/routes.py` |
| 6 | Basic integration test suite | `tests/test_memory/` |

**Outcome:** Stateful conversations that persist across sessions. User preferences remembered.

### Phase 2: Scale (Week 3-4)

| Step | What | Files |
|------|------|-------|
| 1 | Add Semantic Memory (pgvector + embeddings) | `semantic_memory.py` |
| 2 | Add Episodic Memory with partitioning | `episodic_memory.py` |
| 3 | Implement reranking pipeline | `semantic_memory.py` |
| 4 | Add connection pooling (asyncpg) | `config.py` |
| 5 | Add Redis cluster mode | `short_term_memory.py`, `shared_memory.py` |
| 6 | Memory budget monitoring + alerting | `monitoring/` |

**Outcome:** RAG-powered knowledge retrieval. Full event timeline. Production-ready performance.

### Phase 3: Advanced (Week 5-8)

| Step | What | Files |
|------|------|-------|
| 1 | Add Procedural Memory (auto-learn workflows) | `procedural_memory.py` |
| 2 | Add Shared Memory (multi-agent coordination) | `shared_memory.py` |
| 3 | Entity graph overlay (Neo4j) | `entity_memory.py` |
| 4 | Auto entity extraction from conversations | `orchestrator.py` |
| 5 | Memory decay + garbage collection | `long_term_memory.py` |
| 6 | PII detection + encryption pipeline | `security/` |

**Outcome:** Multi-agent system with shared state. Self-learning workflows. Full compliance.

---

## 5. API Endpoints

Base: `/api/v1/memory`

### Long-Term Memory

| Method | Path | Description |
|--------|------|-------------|
| POST | `/long-term/{tenant}/{user}` | Store/update a memory |
| GET | `/long-term/{tenant}/{user}/{key}` | Recall specific memory |
| GET | `/long-term/{tenant}/{user}?q=...` | Search memories |
| DELETE | `/long-term/{tenant}/{user}/{key}` | Forget (GDPR erasure) |

### Entity Memory

| Method | Path | Description |
|--------|------|-------------|
| POST | `/entities/{tenant}` | Create/update entity |
| GET | `/entities/{tenant}/{id}` | Get entity + relationships |
| POST | `/entities/{tenant}/relationships` | Link two entities |
| GET | `/entities/{tenant}?q=...` | Search entities |

### Semantic Memory

| Method | Path | Description |
|--------|------|-------------|
| POST | `/semantic/{tenant}/ingest` | Embed and store chunks |
| POST | `/semantic/{tenant}/search` | Vector/keyword/hybrid search |

### Orchestrator

| Method | Path | Description |
|--------|------|-------------|
| POST | `/orchestrator/{tenant}/assemble` | Assemble full 8-layer context |
| POST | `/orchestrator/{tenant}/post-inference` | Write back after LLM call |

### Memory Middleware Integration

```python
# In FastAPI middleware or dependency
@app.middleware("http")
async def memory_middleware(request: Request, call_next):
    # Extract tenant from JWT
    tenant_id = request.state.tenant_id
    user_id = request.state.user_id
    session_id = request.headers.get("X-Session-ID", "")

    # Inject orchestrator into request state
    request.state.memory = orchestrator

    response = await call_next(request)
    return response
```

---

## 6. Retrieval Strategy

| Scenario | Strategy | Why |
|----------|----------|-----|
| User asks factual question about their data | **Structured query** (Long-Term + Entity) | Exact key lookup, deterministic |
| User asks open-ended knowledge question | **Vector search** (Semantic) | Semantic similarity across documents |
| User asks question with both specific and general aspects | **Hybrid** (Vector + Keyword + Structured) | Best recall with high precision |
| Agent needs to recall a past interaction | **Time-range query** (Episodic) | Temporal filtering on event log |
| Agent needs to find a workflow | **Trigger match** (Procedural) | Pattern matching on trigger conditions |
| Multi-agent needs shared context | **Namespace scan** (Shared) | Direct key-value lookup in Redis |

### Ranking Logic

```
Final Score = 0.7 * vector_similarity
            + 0.3 * keyword_relevance
            + 0.1 * recency_boost
            + 0.1 * access_frequency_boost
            → rerank top 20 → return top 10
```

---

## 7. Personalization Engine

```
Entity Memory (WHO)              Long-Term Memory (WHAT)
    │                                │
    │  user profile                  │  preferences, facts,
    │  relationships                 │  corrections, feedback
    │  interaction history           │  confidence scores
    │                                │
    └───────────┬────────────────────┘
                │
                ▼
    ┌───────────────────────┐
    │  PERSONALIZATION      │
    │  PIPELINE             │
    │                       │
    │  1. Load entity       │
    │  2. Merge preferences │
    │  3. Apply corrections │
    │  4. Inject as system  │
    │     context           │
    │  5. Bias RAG results  │
    │     toward user's     │
    │     domain            │
    └───────────┬───────────┘
                │
                ▼
    Personalized system prompt
    injected into working memory
```

---

## 8. Multi-Agent Coordination

### Shared Memory Design

```
Redis Key Space:
  mem:shared:{tenant}:global:{key}     → global agent state
  mem:shared:{tenant}:{task_group}:{key} → task-specific state
  mem:shared:lock:{tenant}:{ns}:{key}  → distributed locks

Pub/Sub Channels:
  mem:shared:broadcast                 → all-agent notifications
  mem:shared:{tenant}:events           → tenant-scoped events
```

### Task Delegation Flow

```
┌──────────────┐     write task      ┌──────────────────┐
│  Agent A     │ ──────────────────→ │  Shared Memory   │
│  (planner)   │                     │  namespace=task-1 │
└──────────────┘                     └────────┬─────────┘
                                              │
                                    broadcast │ "task-1:assigned"
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                   ┌──────────┐        ┌──────────┐        ┌──────────┐
                   │ Agent B  │        │ Agent C  │        │ Agent D  │
                   │ (coder)  │        │ (tester) │        │ (review) │
                   └────┬─────┘        └────┬─────┘        └────┬─────┘
                        │                   │                    │
                   write result        write result         write result
                        │                   │                    │
                        └───────────────────┼────────────────────┘
                                            ▼
                                   Shared Memory
                                   (conflict resolution)
```

### Conflict Resolution

| Strategy | When | How |
|----------|------|-----|
| **Last-writer-wins** | Non-critical state | Latest timestamp wins |
| **Merge** | Additive state (lists, counters) | Deep-merge values |
| **Reject** | Critical state (locks, transactions) | Return error; agent retries |
| **Version check** | Optimistic concurrency | compare-and-set with version number |

---

## 9. Security & Compliance

### Multi-Tenant Isolation

```sql
-- Every table uses RLS
ALTER TABLE long_term_memory ENABLE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON long_term_memory
    USING (tenant_id = current_setting('app.tenant_id'));

-- Set tenant context per connection
SET app.tenant_id = 'tenant-123';
```

### Encryption

| Layer | At Rest | In Transit |
|-------|---------|------------|
| PostgreSQL | AES-256 (RDS encryption) | TLS 1.3 |
| Redis | AES-256 (ElastiCache encryption) | TLS 1.3 |
| Embeddings | Encrypted with table data | TLS 1.3 |
| Backups | AWS KMS managed keys | N/A |

### PII Handling

1. **Detection**: Guardrails `detect_pii` validator scans all memory writes
2. **Masking**: PII fields stored with reversible masking (encrypted, key in Vault)
3. **Right to erasure**: `DELETE /long-term/{tenant}/{user}/{key}` + cascade to episodic
4. **Retention**: Episodic memory auto-purges after configurable retention period (default: 365 days)
5. **Audit trail**: All memory writes logged to immutable audit table

---

## 10. Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|------------|------------|
| **Memory bloat** | Storage costs spike, queries slow | High | TTLs on short-term, retention policies on episodic, max entries per user on long-term |
| **Context poisoning** | Bad data in memory degrades all future responses | Medium | Confidence scores, source tracking, admin override API, memory "forget" endpoint |
| **Latency spikes** | Slow context assembly blocks LLM calls | Medium | Redis for hot path, connection pooling, async parallel queries, circuit breakers |
| **Cost explosion** | Embedding API costs grow with ingest volume | Medium | Batch embeddings, cache embeddings, use text-embedding-3-small (5x cheaper), chunk dedup |
| **Stale data** | Outdated facts served as current | Medium | `updated_at` tracking, decay scoring, periodic re-validation jobs |
| **Cross-tenant leakage** | Tenant A sees tenant B's data | Critical | RLS on every table, tenant_id in every query, integration tests for isolation |
| **Embedding drift** | Model upgrade changes embedding space | Low | Version embeddings, re-embed on model change, store model ID with chunks |

---

## 11. Cost Model

### Per-Tenant Monthly Estimate (1,000 active users)

| Component | Unit Cost | Usage | Monthly |
|-----------|-----------|-------|---------|
| PostgreSQL (RDS t3.small) | $0.034/hr | 730 hrs | ~$25 |
| Redis (ElastiCache t3.small) | $0.034/hr | 730 hrs | ~$25 |
| Embeddings (text-embedding-3-small) | $0.02/1M tokens | ~5M tokens | ~$0.10 |
| Reranking (Cohere Rerank v3) | $2/1K queries | ~10K queries | ~$20 |
| Storage (gp3 EBS) | $0.08/GB | 50 GB | ~$4 |
| **Total** | | | **~$74/mo** |

### Optimization Tactics

1. **Shared Postgres instance** for L3 + L4 + L6 + L7 — eliminates 3 database bills
2. **pgvector over Pinecone** — saves $70-700/mo for vector DB
3. **Batch embeddings** — 50% cheaper than single-document calls
4. **Embedding cache** — don't re-embed identical content
5. **Redis TTLs** — auto-expire short-term memory instead of manual cleanup
6. **Materialized views** — pre-compute heavy entity+relationship joins
7. **Read replicas** — route read-heavy semantic search to replica

---

## File Map

```
backbone/memory/
├── __init__.py              # Package exports + docstring
├── schemas.py               # Frozen dataclass models for all 8 layers
├── config.py                # Environment-based configuration
├── orchestrator.py          # Main coordinator — assemble + post-inference
├── manager.py               # Legacy 4-tier manager (backward compat)
├── working_memory.py        # L1: Context window management
├── short_term_memory.py     # L2: Redis conversation buffer
├── long_term_memory.py      # L3: PostgreSQL persistent user data
├── episodic_memory.py       # L4: PostgreSQL event timeline
├── semantic_memory.py       # L5: pgvector RAG retrieval
├── procedural_memory.py     # L6: PostgreSQL workflow patterns
├── entity_memory.py         # L7: PostgreSQL + Neo4j entity profiles
├── shared_memory.py         # L8: Redis multi-agent coordination
└── api/
    ├── __init__.py
    └── routes.py            # FastAPI endpoints for all layers
```
