"""Tracer — distributed tracing across agent chains."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any

import structlog

logger = structlog.get_logger("tracer")


@dataclass(frozen=True)
class Span:
    """Immutable trace span."""

    span_id: str
    trace_id: str
    parent_id: str | None
    operation: str
    service: str
    start_time: float
    end_time: float
    status: str = "ok"
    tags: dict[str, str] = field(default_factory=dict)
    events: tuple[dict[str, Any], ...] = field(default_factory=tuple)

    @property
    def duration_ms(self) -> float:
        return (self.end_time - self.start_time) * 1000


class SpanBuilder:
    """Mutable span builder — becomes immutable Span on finish."""

    def __init__(self, trace_id: str, operation: str, service: str, parent_id: str | None = None) -> None:
        self.span_id = str(uuid.uuid4())
        self.trace_id = trace_id
        self.parent_id = parent_id
        self.operation = operation
        self.service = service
        self.start_time = time.time()
        self._tags: dict[str, str] = {}
        self._events: list[dict[str, Any]] = []
        self._status = "ok"

    def tag(self, key: str, value: str) -> SpanBuilder:
        self._tags[key] = value
        return self

    def event(self, name: str, **attrs: Any) -> SpanBuilder:
        self._events.append({"name": name, "time": time.time(), **attrs})
        return self

    def error(self, message: str) -> SpanBuilder:
        self._status = "error"
        self._events.append({"name": "error", "message": message, "time": time.time()})
        return self

    def finish(self) -> Span:
        return Span(
            span_id=self.span_id,
            trace_id=self.trace_id,
            parent_id=self.parent_id,
            operation=self.operation,
            service=self.service,
            start_time=self.start_time,
            end_time=time.time(),
            status=self._status,
            tags=dict(self._tags),
            events=tuple(self._events),
        )


class Tracer:
    """Collects and exports distributed traces across agent execution.

    Provides:
    - Trace correlation across agent chains
    - Span-level timing and status
    - Error tracking with context
    - Export to stdout (dev) or OTLP (prod)
    """

    def __init__(self) -> None:
        self._spans: list[Span] = []

    def start_trace(self, operation: str, service: str = "backbone") -> SpanBuilder:
        """Start a new trace."""
        trace_id = str(uuid.uuid4())
        return SpanBuilder(trace_id=trace_id, operation=operation, service=service)

    def start_span(
        self,
        trace_id: str,
        operation: str,
        service: str = "backbone",
        parent_id: str | None = None,
    ) -> SpanBuilder:
        """Start a child span within an existing trace."""
        return SpanBuilder(
            trace_id=trace_id,
            operation=operation,
            service=service,
            parent_id=parent_id,
        )

    def record(self, span: Span) -> None:
        """Record a completed span."""
        self._spans.append(span)
        logger.info(
            "span_recorded",
            trace_id=span.trace_id,
            span_id=span.span_id,
            operation=span.operation,
            duration_ms=round(span.duration_ms, 2),
            status=span.status,
        )

    def get_trace(self, trace_id: str) -> list[Span]:
        """Get all spans for a trace."""
        return [s for s in self._spans if s.trace_id == trace_id]

    def get_metrics(self) -> dict[str, Any]:
        """Compute aggregate metrics from recorded spans."""
        if not self._spans:
            return {"total_spans": 0}

        durations = [s.duration_ms for s in self._spans]
        errors = [s for s in self._spans if s.status == "error"]

        return {
            "total_spans": len(self._spans),
            "total_traces": len({s.trace_id for s in self._spans}),
            "error_count": len(errors),
            "error_rate": len(errors) / len(self._spans),
            "avg_duration_ms": sum(durations) / len(durations),
            "p95_duration_ms": sorted(durations)[int(len(durations) * 0.95)] if durations else 0,
            "max_duration_ms": max(durations),
        }
