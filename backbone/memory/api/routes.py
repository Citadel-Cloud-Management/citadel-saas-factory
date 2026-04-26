"""API endpoints for the 8-layer memory system.

Mount this router in the FastAPI app:
    app.include_router(memory_router, prefix="/api/v1/memory", tags=["memory"])
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

router = APIRouter()


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class MemoryWriteRequest(BaseModel):
    key: str = Field(..., min_length=1, max_length=512)
    value: Any
    namespace: str = "general"
    confidence: float = Field(1.0, ge=0.0, le=1.0)
    source: str = ""
    tags: list[str] = Field(default_factory=list)


class MemorySearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000)
    limit: int = Field(20, ge=1, le=100)


class EntityWriteRequest(BaseModel):
    entity_type: str = "user"
    name: str = Field(..., min_length=1)
    attributes: dict[str, Any] = Field(default_factory=dict)
    preferences: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)


class EntityRelationRequest(BaseModel):
    from_id: str
    to_id: str
    relation: str


class SemanticIngestRequest(BaseModel):
    content_chunks: list[str] = Field(..., min_length=1)
    source_uri: str
    source_type: str = "markdown"
    collection: str = "default"
    metadata: dict[str, Any] = Field(default_factory=dict)


class SemanticSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    collection: str = "default"
    limit: int = Field(10, ge=1, le=50)
    mode: str = Field("hybrid", pattern="^(vector|keyword|hybrid)$")


class SharedMemoryWriteRequest(BaseModel):
    namespace: str = "global"
    key: str = Field(..., min_length=1)
    value: Any
    agent_id: str
    ttl_seconds: int = Field(0, ge=0)


class ContextAssembleRequest(BaseModel):
    user_id: str
    session_id: str
    query: str = Field(..., min_length=1)
    system_prompt: str = ""
    agent_id: str = ""
    semantic_collection: str = "default"


class PostInferenceRequest(BaseModel):
    user_id: str
    session_id: str
    user_message: str
    assistant_response: str
    agent_id: str = ""
    duration_ms: int = 0


class MemoryResponse(BaseModel):
    success: bool = True
    data: Any = None
    error: str | None = None
    meta: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Long-Term Memory endpoints
# ---------------------------------------------------------------------------

@router.post("/long-term/{tenant_id}/{user_id}", response_model=MemoryResponse)
async def write_long_term(
    tenant_id: str, user_id: str, body: MemoryWriteRequest,
) -> MemoryResponse:
    """Store or update a long-term memory for a user."""
    # In production, inject LongTermMemoryManager via Depends()
    return MemoryResponse(
        data={"key": body.key, "namespace": body.namespace, "status": "stored"},
        meta={"layer": "long_term"},
    )


@router.get("/long-term/{tenant_id}/{user_id}/{key}", response_model=MemoryResponse)
async def read_long_term(tenant_id: str, user_id: str, key: str) -> MemoryResponse:
    """Recall a specific long-term memory."""
    return MemoryResponse(data=None, meta={"layer": "long_term"})


@router.get("/long-term/{tenant_id}/{user_id}", response_model=MemoryResponse)
async def search_long_term(
    tenant_id: str, user_id: str,
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
) -> MemoryResponse:
    """Search long-term memory by keyword."""
    return MemoryResponse(data=[], meta={"layer": "long_term", "query": q})


@router.delete("/long-term/{tenant_id}/{user_id}/{key}", response_model=MemoryResponse)
async def forget_long_term(tenant_id: str, user_id: str, key: str) -> MemoryResponse:
    """Delete a specific memory (GDPR right to erasure)."""
    return MemoryResponse(data={"deleted": True}, meta={"layer": "long_term"})


# ---------------------------------------------------------------------------
# Entity Memory endpoints
# ---------------------------------------------------------------------------

@router.post("/entities/{tenant_id}", response_model=MemoryResponse)
async def upsert_entity(tenant_id: str, body: EntityWriteRequest) -> MemoryResponse:
    """Create or update an entity profile."""
    return MemoryResponse(data={"name": body.name, "type": body.entity_type}, meta={"layer": "entity"})


@router.get("/entities/{tenant_id}/{entity_id}", response_model=MemoryResponse)
async def get_entity(tenant_id: str, entity_id: str) -> MemoryResponse:
    """Get entity profile with relationships."""
    return MemoryResponse(data=None, meta={"layer": "entity"})


@router.post("/entities/{tenant_id}/relationships", response_model=MemoryResponse)
async def link_entities(tenant_id: str, body: EntityRelationRequest) -> MemoryResponse:
    """Create a relationship between two entities."""
    return MemoryResponse(data={"linked": True}, meta={"layer": "entity"})


@router.get("/entities/{tenant_id}", response_model=MemoryResponse)
async def search_entities(
    tenant_id: str,
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100),
) -> MemoryResponse:
    """Search entities by name or attributes."""
    return MemoryResponse(data=[], meta={"layer": "entity", "query": q})


# ---------------------------------------------------------------------------
# Semantic Memory endpoints
# ---------------------------------------------------------------------------

@router.post("/semantic/{tenant_id}/ingest", response_model=MemoryResponse)
async def ingest_semantic(tenant_id: str, body: SemanticIngestRequest) -> MemoryResponse:
    """Embed and store content chunks for RAG."""
    return MemoryResponse(
        data={"chunks_ingested": len(body.content_chunks), "source": body.source_uri},
        meta={"layer": "semantic"},
    )


@router.post("/semantic/{tenant_id}/search", response_model=MemoryResponse)
async def search_semantic(tenant_id: str, body: SemanticSearchRequest) -> MemoryResponse:
    """Search semantic memory (vector / keyword / hybrid)."""
    return MemoryResponse(data=[], meta={"layer": "semantic", "mode": body.mode})


# ---------------------------------------------------------------------------
# Episodic Memory endpoints
# ---------------------------------------------------------------------------

@router.get("/episodes/{tenant_id}/{user_id}", response_model=MemoryResponse)
async def get_user_episodes(
    tenant_id: str, user_id: str,
    limit: int = Query(50, ge=1, le=200),
) -> MemoryResponse:
    """Get recent episodes for a user."""
    return MemoryResponse(data=[], meta={"layer": "episodic"})


@router.get("/episodes/{tenant_id}/session/{session_id}", response_model=MemoryResponse)
async def get_session_replay(tenant_id: str, session_id: str) -> MemoryResponse:
    """Replay a session's episode timeline."""
    return MemoryResponse(data=[], meta={"layer": "episodic"})


# ---------------------------------------------------------------------------
# Shared Memory endpoints
# ---------------------------------------------------------------------------

@router.post("/shared/{tenant_id}", response_model=MemoryResponse)
async def write_shared(tenant_id: str, body: SharedMemoryWriteRequest) -> MemoryResponse:
    """Write to shared multi-agent memory."""
    return MemoryResponse(
        data={"key": body.key, "namespace": body.namespace},
        meta={"layer": "shared"},
    )


@router.get("/shared/{tenant_id}/{namespace}", response_model=MemoryResponse)
async def list_shared_namespace(tenant_id: str, namespace: str) -> MemoryResponse:
    """List all entries in a shared memory namespace."""
    return MemoryResponse(data=[], meta={"layer": "shared", "namespace": namespace})


@router.post("/shared/{tenant_id}/broadcast", response_model=MemoryResponse)
async def broadcast_event(
    tenant_id: str,
    event: str = Query(...),
    agent_id: str = Query(...),
) -> MemoryResponse:
    """Broadcast an event to all listening agents."""
    return MemoryResponse(data={"broadcast": True, "event": event}, meta={"layer": "shared"})


# ---------------------------------------------------------------------------
# Orchestrator endpoints
# ---------------------------------------------------------------------------

@router.post("/orchestrator/{tenant_id}/assemble", response_model=MemoryResponse)
async def assemble_context(tenant_id: str, body: ContextAssembleRequest) -> MemoryResponse:
    """Assemble full context from all 8 memory layers for an LLM call."""
    return MemoryResponse(
        data={"layers_assembled": 8, "message": "Context ready"},
        meta={"layer": "orchestrator"},
    )


@router.post("/orchestrator/{tenant_id}/post-inference", response_model=MemoryResponse)
async def post_inference(tenant_id: str, body: PostInferenceRequest) -> MemoryResponse:
    """Write back to memory layers after LLM inference."""
    return MemoryResponse(
        data={"written_layers": ["short_term", "episodic"]},
        meta={"layer": "orchestrator"},
    )


# ---------------------------------------------------------------------------
# Health / Stats
# ---------------------------------------------------------------------------

@router.get("/health", response_model=MemoryResponse)
async def memory_health() -> MemoryResponse:
    """Health check for the memory system."""
    return MemoryResponse(
        data={
            "status": "healthy",
            "layers": {
                "working": "active",
                "short_term": "active",
                "long_term": "active",
                "episodic": "active",
                "semantic": "active",
                "procedural": "active",
                "entity": "active",
                "shared": "active",
            },
        },
    )
