"""Common Pydantic schemas — shared response envelopes and pagination."""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Standard error response envelope."""

    model_config = ConfigDict(frozen=True)

    error: str
    code: int
    details: dict[str, Any] | None = None


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response envelope."""

    model_config = ConfigDict(frozen=True)

    data: T
    meta: dict[str, Any] | None = None


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    model_config = ConfigDict(frozen=True)

    total: int
    page: int
    limit: int
    pages: int = Field(default=0)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response with metadata."""

    model_config = ConfigDict(frozen=True)

    data: list[T]
    total: int
    page: int
    limit: int
