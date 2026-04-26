"""Layer 7: Entity Memory — structured profiles for users, orgs, products, agents.

Relational storage in PostgreSQL with optional graph overlay (Neo4j) for
relationship traversal. Supports automatic entity extraction from conversations.
"""

from __future__ import annotations

from typing import Any, Protocol

import structlog

from backbone.memory.config import EntityConfig
from backbone.memory.schemas import EntityProfile, EntityType

logger = structlog.get_logger("memory.entity")


class EntityBackend(Protocol):
    """Backend interface for entity storage."""

    async def upsert(self, profile: EntityProfile) -> None: ...
    async def get(self, tenant_id: str, entity_id: str) -> EntityProfile | None: ...
    async def find_by_type(self, tenant_id: str, entity_type: EntityType, limit: int) -> list[EntityProfile]: ...
    async def find_by_name(self, tenant_id: str, name: str) -> list[EntityProfile]: ...
    async def get_relationships(self, tenant_id: str, entity_id: str) -> list[dict[str, str]]: ...
    async def add_relationship(
        self, tenant_id: str, from_id: str, to_id: str, relation: str,
    ) -> None: ...
    async def search(self, tenant_id: str, query: str, limit: int) -> list[EntityProfile]: ...
    async def delete(self, tenant_id: str, entity_id: str) -> bool: ...


class PostgresEntityBackend:
    """PostgreSQL-backed entity memory.

    Schema:

    CREATE TABLE entity_profiles (
        entity_id          TEXT PRIMARY KEY,
        tenant_id          TEXT NOT NULL,
        entity_type        TEXT NOT NULL,
        name               TEXT NOT NULL,
        attributes         JSONB DEFAULT '{}',
        preferences        JSONB DEFAULT '{}',
        history_summary    TEXT DEFAULT '',
        first_seen_at      TIMESTAMPTZ DEFAULT now(),
        last_seen_at       TIMESTAMPTZ DEFAULT now(),
        interaction_count  INTEGER DEFAULT 0,
        tags               TEXT[] DEFAULT '{}'
    );

    CREATE TABLE entity_relationships (
        id          SERIAL PRIMARY KEY,
        tenant_id   TEXT NOT NULL,
        from_id     TEXT NOT NULL REFERENCES entity_profiles(entity_id),
        to_id       TEXT NOT NULL REFERENCES entity_profiles(entity_id),
        relation    TEXT NOT NULL,
        created_at  TIMESTAMPTZ DEFAULT now(),
        UNIQUE(tenant_id, from_id, to_id, relation)
    );

    CREATE INDEX idx_ent_tenant_type ON entity_profiles(tenant_id, entity_type);
    CREATE INDEX idx_ent_name ON entity_profiles(tenant_id, name);
    CREATE INDEX idx_ent_attrs ON entity_profiles USING GIN(attributes);
    CREATE INDEX idx_rel_from ON entity_relationships(tenant_id, from_id);
    CREATE INDEX idx_rel_to ON entity_relationships(tenant_id, to_id);

    ALTER TABLE entity_profiles ENABLE ROW LEVEL SECURITY;
    CREATE POLICY tenant_isolation ON entity_profiles
        USING (tenant_id = current_setting('app.tenant_id'));
    ALTER TABLE entity_relationships ENABLE ROW LEVEL SECURITY;
    CREATE POLICY tenant_isolation ON entity_relationships
        USING (tenant_id = current_setting('app.tenant_id'));
    """

    def __init__(self, pool: Any) -> None:
        self._pool = pool

    async def upsert(self, profile: EntityProfile) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO entity_profiles
                    (entity_id, tenant_id, entity_type, name, attributes,
                     preferences, history_summary, first_seen_at, last_seen_at,
                     interaction_count, tags)
                VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11)
                ON CONFLICT (entity_id) DO UPDATE SET
                    name = EXCLUDED.name,
                    attributes = entity_profiles.attributes || EXCLUDED.attributes,
                    preferences = entity_profiles.preferences || EXCLUDED.preferences,
                    last_seen_at = now(),
                    interaction_count = entity_profiles.interaction_count + 1,
                    tags = EXCLUDED.tags
                """,
                profile.entity_id, profile.tenant_id, profile.entity_type.value,
                profile.name, profile.attributes, profile.preferences,
                profile.history_summary, profile.first_seen_at,
                profile.last_seen_at, profile.interaction_count,
                list(profile.tags),
            )

    async def get(self, tenant_id: str, entity_id: str) -> EntityProfile | None:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT * FROM entity_profiles WHERE tenant_id = $1 AND entity_id = $2",
                tenant_id, entity_id,
            )
            return self._row_to_profile(row) if row else None

    async def find_by_type(self, tenant_id: str, entity_type: EntityType, limit: int) -> list[EntityProfile]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM entity_profiles
                WHERE tenant_id = $1 AND entity_type = $2
                ORDER BY interaction_count DESC LIMIT $3
                """,
                tenant_id, entity_type.value, limit,
            )
            return [self._row_to_profile(r) for r in rows]

    async def find_by_name(self, tenant_id: str, name: str) -> list[EntityProfile]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT * FROM entity_profiles WHERE tenant_id = $1 AND name ILIKE $2",
                tenant_id, f"%{name}%",
            )
            return [self._row_to_profile(r) for r in rows]

    async def get_relationships(self, tenant_id: str, entity_id: str) -> list[dict[str, str]]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT r.relation, r.to_id, e.name, e.entity_type
                FROM entity_relationships r
                JOIN entity_profiles e ON r.to_id = e.entity_id
                WHERE r.tenant_id = $1 AND r.from_id = $2
                """,
                tenant_id, entity_id,
            )
            return [
                {"relation": r["relation"], "to_id": r["to_id"],
                 "name": r["name"], "type": r["entity_type"]}
                for r in rows
            ]

    async def add_relationship(
        self, tenant_id: str, from_id: str, to_id: str, relation: str,
    ) -> None:
        async with self._pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO entity_relationships (tenant_id, from_id, to_id, relation)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (tenant_id, from_id, to_id, relation) DO NOTHING
                """,
                tenant_id, from_id, to_id, relation,
            )

    async def search(self, tenant_id: str, query: str, limit: int) -> list[EntityProfile]:
        async with self._pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT * FROM entity_profiles
                WHERE tenant_id = $1
                  AND (name ILIKE $2 OR attributes::text ILIKE $2)
                ORDER BY interaction_count DESC LIMIT $3
                """,
                tenant_id, f"%{query}%", limit,
            )
            return [self._row_to_profile(r) for r in rows]

    async def delete(self, tenant_id: str, entity_id: str) -> bool:
        async with self._pool.acquire() as conn:
            await conn.execute(
                "DELETE FROM entity_relationships WHERE tenant_id = $1 AND (from_id = $2 OR to_id = $2)",
                tenant_id, entity_id,
            )
            result = await conn.execute(
                "DELETE FROM entity_profiles WHERE tenant_id = $1 AND entity_id = $2",
                tenant_id, entity_id,
            )
            return result == "DELETE 1"

    @staticmethod
    def _row_to_profile(row: Any) -> EntityProfile:
        return EntityProfile(
            entity_id=row["entity_id"],
            tenant_id=row["tenant_id"],
            entity_type=EntityType(row["entity_type"]),
            name=row["name"],
            attributes=row["attributes"],
            preferences=row["preferences"],
            history_summary=row["history_summary"],
            first_seen_at=str(row["first_seen_at"]),
            last_seen_at=str(row["last_seen_at"]),
            interaction_count=row["interaction_count"],
            tags=tuple(row["tags"]),
        )


class EntityMemoryManager:
    """Manages structured entity profiles and relationships.

    Combines with long-term memory for personalization:
    - Entity memory = WHO (structured profiles)
    - Long-term memory = WHAT (learned facts and preferences)
    - Together = personalized, context-aware responses
    """

    def __init__(self, config: EntityConfig, backend: EntityBackend) -> None:
        self._config = config
        self._backend = backend

    async def upsert_entity(
        self,
        tenant_id: str,
        entity_type: EntityType,
        name: str,
        attributes: dict[str, Any] | None = None,
        preferences: dict[str, Any] | None = None,
        entity_id: str | None = None,
        tags: tuple[str, ...] = (),
    ) -> EntityProfile:
        """Create or update an entity profile."""
        profile = EntityProfile(
            entity_id=entity_id or "",
            tenant_id=tenant_id,
            entity_type=entity_type,
            name=name,
            attributes=attributes or {},
            preferences=preferences or {},
            tags=tags,
        )
        await self._backend.upsert(profile)
        logger.info("entity_upserted", name=name, type=entity_type.value)
        return profile

    async def get_entity(self, tenant_id: str, entity_id: str) -> EntityProfile | None:
        return await self._backend.get(tenant_id, entity_id)

    async def get_with_relationships(self, tenant_id: str, entity_id: str) -> dict[str, Any]:
        """Get entity profile with all its relationships."""
        profile = await self._backend.get(tenant_id, entity_id)
        if not profile:
            return {}
        relationships = await self._backend.get_relationships(tenant_id, entity_id)
        return {
            "profile": profile,
            "relationships": relationships,
        }

    async def link_entities(
        self, tenant_id: str, from_id: str, to_id: str, relation: str,
    ) -> None:
        """Create a relationship between two entities."""
        await self._backend.add_relationship(tenant_id, from_id, to_id, relation)
        logger.info("entity_linked", from_id=from_id, to_id=to_id, relation=relation)

    async def search_entities(self, tenant_id: str, query: str, limit: int = 20) -> list[EntityProfile]:
        return await self._backend.search(tenant_id, query, limit)

    async def delete_entity(self, tenant_id: str, entity_id: str) -> bool:
        """Delete an entity and all its relationships (GDPR erasure)."""
        deleted = await self._backend.delete(tenant_id, entity_id)
        if deleted:
            logger.info("entity_deleted", entity_id=entity_id)
        return deleted
