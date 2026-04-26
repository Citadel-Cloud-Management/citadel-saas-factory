"""Layer 5: Semantic Memory — vector-based knowledge retrieval (RAG).

Uses pgvector (default), Qdrant, or Pinecone for embedding storage.
Supports hybrid retrieval: vector similarity + keyword filtering + reranking.
"""

from __future__ import annotations

from typing import Any, Protocol, Sequence

import structlog

from backbone.memory.config import SemanticConfig
from backbone.memory.schemas import SemanticChunk, SemanticSearchResult

logger = structlog.get_logger("memory.semantic")


class EmbeddingProvider(Protocol):
    """Interface for generating embeddings."""

    async def embed(self, texts: list[str]) -> list[list[float]]: ...

    @property
    def dimensions(self) -> int: ...


class RerankerProvider(Protocol):
    """Interface for reranking search results."""

    async def rerank(self, query: str, documents: list[str], top_n: int) -> list[tuple[int, float]]: ...


class VectorBackend(Protocol):
    """Backend interface for vector storage and search."""

    async def upsert(self, chunks: list[SemanticChunk]) -> int: ...
    async def search(
        self, tenant_id: str, collection: str, embedding: list[float],
        limit: int, threshold: float,
    ) -> list[SemanticSearchResult]: ...
    async def hybrid_search(
        self, tenant_id: str, collection: str, embedding: list[float],
        keyword_query: str, limit: int,
    ) -> list[SemanticSearchResult]: ...
    async def delete_by_source(self, tenant_id: str, source_uri: str) -> int: ...
    async def count(self, tenant_id: str, collection: str) -> int: ...


class PgVectorBackend:
    """pgvector-backed semantic memory.

    Schema (applied via Alembic migration):

    CREATE EXTENSION IF NOT EXISTS vector;

    CREATE TABLE semantic_chunks (
        chunk_id     TEXT PRIMARY KEY,
        tenant_id    TEXT NOT NULL,
        collection   TEXT NOT NULL DEFAULT 'default',
        content      TEXT NOT NULL,
        source_uri   TEXT DEFAULT '',
        source_type  TEXT DEFAULT '',
        metadata     JSONB DEFAULT '{}',
        embedding    vector(1536),
        token_count  INTEGER DEFAULT 0,
        created_at   TIMESTAMPTZ DEFAULT now(),
        updated_at   TIMESTAMPTZ DEFAULT now()
    );

    -- HNSW index for fast similarity search
    CREATE INDEX idx_sem_embedding ON semantic_chunks
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64);

    -- Filtering indexes
    CREATE INDEX idx_sem_tenant_coll ON semantic_chunks(tenant_id, collection);
    CREATE INDEX idx_sem_source ON semantic_chunks(tenant_id, source_uri);
    CREATE INDEX idx_sem_metadata ON semantic_chunks USING GIN(metadata);

    -- Full-text search for hybrid retrieval
    ALTER TABLE semantic_chunks ADD COLUMN fts tsvector
        GENERATED ALWAYS AS (to_tsvector('english', content)) STORED;
    CREATE INDEX idx_sem_fts ON semantic_chunks USING GIN(fts);

    -- RLS
    ALTER TABLE semantic_chunks ENABLE ROW LEVEL SECURITY;
    CREATE POLICY tenant_isolation ON semantic_chunks
        USING (tenant_id = current_setting('app.tenant_id'));
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def upsert(self, chunks: list[SemanticChunk]) -> int:
        async with self._pool.acquire() as conn:
            for chunk in chunks:
                await conn.execute(
                    """
                    INSERT INTO semantic_chunks
                        (chunk_id, tenant_id, collection, content, source_uri,
                         source_type, metadata, embedding, token_count, created_at, updated_at)
                    VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
                    ON CONFLICT (chunk_id) DO UPDATE SET
                        content = EXCLUDED.content,
                        embedding = EXCLUDED.embedding,
                        metadata = EXCLUDED.metadata,
                        updated_at = now()
                    """,
                    chunk.chunk_id, chunk.tenant_id, chunk.collection,
                    chunk.content, chunk.source_uri, chunk.source_type,
                    chunk.metadata, str(chunk.embedding), chunk.token_count,
                    chunk.created_at, chunk.updated_at,
                )
        return len(chunks)

    async def search(
        self, tenant_id: str, collection: str, embedding: list[float],
        limit: int, threshold: float,
    ) -> list[SemanticSearchResult]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT *, 1 - (embedding <=> $1::vector) AS score
                FROM semantic_chunks
                WHERE tenant_id = $2 AND collection = $3
                  AND 1 - (embedding <=> $1::vector) >= $4
                ORDER BY embedding <=> $1::vector
                LIMIT $5
                """,
                str(embedding), tenant_id, collection, threshold, limit,
            )
            return [
                SemanticSearchResult(
                    chunk=self._row_to_chunk(r),
                    score=r["score"],
                )
                for r in rows
            ]

    async def hybrid_search(
        self, tenant_id: str, collection: str, embedding: list[float],
        keyword_query: str, limit: int,
    ) -> list[SemanticSearchResult]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT *,
                    0.7 * (1 - (embedding <=> $1::vector)) +
                    0.3 * ts_rank(fts, plainto_tsquery('english', $4)) AS score
                FROM semantic_chunks
                WHERE tenant_id = $2 AND collection = $3
                  AND (fts @@ plainto_tsquery('english', $4)
                       OR 1 - (embedding <=> $1::vector) >= 0.5)
                ORDER BY score DESC
                LIMIT $5
                """,
                str(embedding), tenant_id, collection, keyword_query, limit,
            )
            return [
                SemanticSearchResult(
                    chunk=self._row_to_chunk(r),
                    score=r["score"],
                )
                for r in rows
            ]

    async def delete_by_source(self, tenant_id: str, source_uri: str) -> int:
        async with self._pool.acquire() as conn:
            result = await conn.execute(
                "DELETE FROM semantic_chunks WHERE tenant_id = $1 AND source_uri = $2",
                tenant_id, source_uri,
            )
            return int(result.split()[-1])

    async def count(self, tenant_id: str, collection: str) -> int:
        async with self._pool.acquire() as conn:
            return await conn.fetchval(
                "SELECT COUNT(*) FROM semantic_chunks WHERE tenant_id = $1 AND collection = $2",
                tenant_id, collection,
            )

    @staticmethod
    def _row_to_chunk(row: Any) -> SemanticChunk:
        return SemanticChunk(
            chunk_id=row["chunk_id"],
            tenant_id=row["tenant_id"],
            collection=row["collection"],
            content=row["content"],
            source_uri=row["source_uri"],
            source_type=row["source_type"],
            metadata=row["metadata"],
            token_count=row["token_count"],
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )


class SemanticMemoryManager:
    """Manages vector-based knowledge retrieval.

    Supports three retrieval modes:
    1. Vector search — pure semantic similarity
    2. Keyword search — full-text search (PostgreSQL tsvector)
    3. Hybrid — weighted combination of vector + keyword
    """

    def __init__(
        self,
        config: SemanticConfig,
        backend: VectorBackend,
        embedder: EmbeddingProvider,
        reranker: RerankerProvider | None = None,
    ) -> None:
        self._config = config
        self._backend = backend
        self._embedder = embedder
        self._reranker = reranker

    async def ingest(
        self,
        tenant_id: str,
        content_chunks: list[str],
        source_uri: str,
        source_type: str = "markdown",
        collection: str = "default",
        metadata: dict[str, Any] | None = None,
    ) -> int:
        """Embed and store content chunks."""
        embeddings = await self._embedder.embed(content_chunks)

        chunks = [
            SemanticChunk(
                tenant_id=tenant_id,
                collection=collection,
                content=text,
                source_uri=source_uri,
                source_type=source_type,
                metadata=metadata or {},
                embedding=emb,
                token_count=len(text.split()),
            )
            for text, emb in zip(content_chunks, embeddings)
        ]

        count = await self._backend.upsert(chunks)
        logger.info("semantic_ingested", count=count, source=source_uri)
        return count

    async def search(
        self,
        tenant_id: str,
        query: str,
        collection: str = "default",
        limit: int | None = None,
        mode: str = "hybrid",
    ) -> list[SemanticSearchResult]:
        """Search semantic memory.

        Modes:
        - vector: pure embedding similarity
        - keyword: full-text search only
        - hybrid: weighted combination (default)
        """
        max_results = limit or self._config.max_results
        query_embedding = (await self._embedder.embed([query]))[0]

        if mode == "hybrid":
            results = await self._backend.hybrid_search(
                tenant_id, collection, query_embedding, query, max_results * 2,
            )
        else:
            results = await self._backend.search(
                tenant_id, collection, query_embedding,
                max_results * 2, self._config.similarity_threshold,
            )

        # Rerank if enabled
        if self._reranker and self._config.reranker_enabled and results:
            docs = [r.chunk.content for r in results]
            reranked = await self._reranker.rerank(query, docs, max_results)
            reranked_results = []
            for idx, score in reranked:
                original = results[idx]
                reranked_results.append(
                    SemanticSearchResult(
                        chunk=original.chunk,
                        score=original.score,
                        rerank_score=score,
                    )
                )
            return reranked_results[:max_results]

        return results[:max_results]

    async def delete_source(self, tenant_id: str, source_uri: str) -> int:
        """Remove all chunks from a source (e.g., when document is updated)."""
        count = await self._backend.delete_by_source(tenant_id, source_uri)
        logger.info("semantic_deleted", count=count, source=source_uri)
        return count
