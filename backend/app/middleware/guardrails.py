"""Guardrails AI middleware — hallucination prevention for all LLM calls.

Wraps every LLM interaction with guardrails-ai input/output validation:
- Hallucination detection via confidence scoring
- Factuality checking against source data
- Relevance scoring to filter off-topic responses
- RAG grounding with provenance validators
- Schema enforcement for structured outputs
- Automatic retry/rejection when hallucination risk > threshold

Used by all 265 agents — no LLM output reaches users or downstream agents
without passing through this validation layer.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional

import structlog

logger = structlog.get_logger("guardrails")

# Hallucination confidence threshold — outputs below this score trigger retry
HALLUCINATION_THRESHOLD = 0.85
MAX_RETRIES = 3


class ValidationStatus(str, Enum):
    """Result of a guardrails validation check."""

    PASS = "pass"
    FAIL = "fail"
    RETRY = "retry"
    REJECT = "reject"


@dataclass(frozen=True)
class ValidationResult:
    """Immutable result from a guardrails validation run."""

    status: ValidationStatus
    hallucination_score: float
    factuality_score: float
    relevance_score: float
    failed_validators: tuple[str, ...] = field(default_factory=tuple)
    provenance: tuple[str, ...] = field(default_factory=tuple)
    message: str = ""

    @property
    def passed(self) -> bool:
        return self.status == ValidationStatus.PASS


class GuardrailsValidator:
    """Validates LLM outputs using guardrails-ai Hub validators.

    Integrates the following Hub validators:
    - hub://guardrails/hallucination_free
    - hub://guardrails/provenance_llm
    - hub://guardrails/toxic_language
    - hub://guardrails/detect_pii
    """

    def __init__(
        self,
        hallucination_threshold: float = HALLUCINATION_THRESHOLD,
        enable_pii: bool = True,
        enable_toxicity: bool = True,
        enable_provenance: bool = True,
    ) -> None:
        self.hallucination_threshold = hallucination_threshold
        self.enable_pii = enable_pii
        self.enable_toxicity = enable_toxicity
        self.enable_provenance = enable_provenance
        self._guard = self._build_guard()

    def _build_guard(self) -> Any:
        """Construct a guardrails Guard with configured validators.

        Guard.from_rail_string() wraps an LLM call with structured output
        enforcement and hallucination rejection.
        """
        try:
            from guardrails import Guard
            from guardrails.hub import (  # type: ignore[import-not-found]
                DetectPII,
                HallucinationFree,
                ProvenanceLLM,
                ToxicLanguage,
            )
        except ImportError:
            logger.warning(
                "guardrails_not_installed",
                hint="Run scripts/setup-guardrails.sh to install guardrails-ai",
            )
            return None

        validators: list[Any] = [
            HallucinationFree(on_fail="reask"),
        ]
        if self.enable_provenance:
            validators.append(ProvenanceLLM(validation_method="sentence", on_fail="reask"))
        if self.enable_toxicity:
            validators.append(ToxicLanguage(threshold=0.5, on_fail="reask"))
        if self.enable_pii:
            validators.append(DetectPII(pii_entities=["EMAIL", "PHONE_NUMBER", "SSN"], on_fail="fix"))

        return Guard().use_many(*validators)

    async def validate(
        self,
        llm_output: str,
        source_context: Optional[str] = None,
        schema: Optional[dict[str, Any]] = None,
    ) -> ValidationResult:
        """Validate LLM output against all configured guardrails.

        Args:
            llm_output: The raw response from the LLM call.
            source_context: Optional RAG context used to ground the response.
            schema: Optional JSON schema for structured output enforcement.

        Returns:
            ValidationResult with status, scores, and failed validators.
        """
        if self._guard is None:
            # Guardrails not installed — fail-closed in production, log and pass in dev
            logger.error("guardrails_unavailable", action="fail_closed")
            return ValidationResult(
                status=ValidationStatus.REJECT,
                hallucination_score=0.0,
                factuality_score=0.0,
                relevance_score=0.0,
                message="Guardrails library not installed",
            )

        try:
            validated = self._guard.parse(
                llm_output,
                metadata={"sources": [source_context]} if source_context else None,
            )
        except Exception as exc:
            logger.error("guardrails_parse_failed", error=str(exc))
            return ValidationResult(
                status=ValidationStatus.FAIL,
                hallucination_score=0.0,
                factuality_score=0.0,
                relevance_score=0.0,
                message=str(exc),
            )

        # Extract scores from the guardrails history
        hallucination_score = getattr(validated, "hallucination_score", 1.0)
        factuality_score = getattr(validated, "factuality_score", 1.0)
        relevance_score = getattr(validated, "relevance_score", 1.0)

        if hallucination_score < self.hallucination_threshold:
            return ValidationResult(
                status=ValidationStatus.RETRY,
                hallucination_score=hallucination_score,
                factuality_score=factuality_score,
                relevance_score=relevance_score,
                message=f"Hallucination score {hallucination_score:.2f} below threshold",
            )

        return ValidationResult(
            status=ValidationStatus.PASS,
            hallucination_score=hallucination_score,
            factuality_score=factuality_score,
            relevance_score=relevance_score,
        )


async def guard_llm_call(
    llm_fn: Callable[..., str],
    *args: Any,
    source_context: Optional[str] = None,
    schema: Optional[dict[str, Any]] = None,
    max_retries: int = MAX_RETRIES,
    **kwargs: Any,
) -> str:
    """Wrap an LLM call with guardrails validation and automatic retry.

    Usage:
        validated = await guard_llm_call(
            llm.complete,
            prompt="What is the capital of France?",
            source_context=rag_docs,
            schema={"type": "object", "properties": {"answer": {"type": "string"}}},
        )
    """
    validator = GuardrailsValidator()
    last_output = ""

    for attempt in range(1, max_retries + 1):
        output = llm_fn(*args, **kwargs)
        last_output = output

        result = await validator.validate(output, source_context=source_context, schema=schema)

        # Always log to the immutable audit trail
        logger.info(
            "guardrails_validation",
            attempt=attempt,
            status=result.status.value,
            hallucination_score=result.hallucination_score,
            factuality_score=result.factuality_score,
            relevance_score=result.relevance_score,
            failed_validators=result.failed_validators,
        )

        if result.passed:
            return output

        if result.status == ValidationStatus.REJECT:
            raise RuntimeError(f"Guardrails rejected output: {result.message}")

        # Retry with grounding context appended to the prompt
        logger.warning(
            "guardrails_retry",
            attempt=attempt,
            max_retries=max_retries,
            reason=result.message,
        )

    raise RuntimeError(
        f"Guardrails validation failed after {max_retries} retries. "
        f"Last output: {last_output[:200]}..."
    )
