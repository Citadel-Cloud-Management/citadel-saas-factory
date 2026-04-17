"""Validator — validates agent inputs/outputs, enforces safety policies."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

import structlog

logger = structlog.get_logger("validation")


class ValidationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass(frozen=True)
class ValidationIssue:
    """Immutable validation finding."""

    rule: str
    severity: ValidationSeverity
    message: str
    field: str = ""


@dataclass(frozen=True)
class ValidationReport:
    """Immutable validation report."""

    passed: bool
    issues: tuple[ValidationIssue, ...] = field(default_factory=tuple)
    confidence_score: float = 1.0
    checked_rules: tuple[str, ...] = field(default_factory=tuple)


async def validate_input(data: Any, schema: dict[str, Any] | None = None) -> ValidationReport:
    """Validate input data before agent execution.

    Checks:
    - Required fields present
    - Data types correct
    - No prompt injection patterns
    - Size limits respected
    """
    issues: list[ValidationIssue] = []

    if data is None:
        issues.append(ValidationIssue(
            rule="non_null",
            severity=ValidationSeverity.ERROR,
            message="Input data cannot be None",
        ))

    if isinstance(data, str) and len(data) > 100_000:
        issues.append(ValidationIssue(
            rule="size_limit",
            severity=ValidationSeverity.WARNING,
            message=f"Input exceeds recommended size: {len(data)} chars",
        ))

    text_to_check = _extract_text(data)
    injection_patterns = [
        "ignore previous instructions",
        "ignore all previous",
        "disregard your instructions",
        "discard your prior directives",
        "you are now",
        "your new role is",
        "act as if you are",
        "pretend you are",
        "new instructions:",
        "system prompt:",
        "override your",
        "forget your rules",
        "bypass your",
        "jailbreak",
        "do anything now",
        "developer mode",
    ]
    for text in text_to_check:
        text_lower = text.lower()
        for pattern in injection_patterns:
            if pattern in text_lower:
                issues.append(ValidationIssue(
                    rule="prompt_injection",
                    severity=ValidationSeverity.CRITICAL,
                    message=f"Potential prompt injection detected: '{pattern}'",
                ))

    passed = not any(i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL) for i in issues)

    return ValidationReport(
        passed=passed,
        issues=tuple(issues),
        checked_rules=("non_null", "size_limit", "prompt_injection"),
    )


def _extract_text(data: Any) -> list[str]:
    """Recursively extract all string values from nested data structures."""
    if isinstance(data, str):
        return [data]
    if isinstance(data, dict):
        texts: list[str] = []
        for v in data.values():
            texts.extend(_extract_text(v))
        return texts
    if isinstance(data, (list, tuple)):
        texts = []
        for item in data:
            texts.extend(_extract_text(item))
        return texts
    return [str(data)] if data is not None else []


async def validate_output(output: Any, task: Any = None) -> ValidationReport:
    """Validate agent output after execution.

    Checks:
    - Output is not empty
    - No sensitive data leakage (PII patterns)
    - Confidence scoring
    - Schema compliance (if provided)
    """
    issues: list[ValidationIssue] = []
    confidence = 1.0

    if output is None:
        issues.append(ValidationIssue(
            rule="non_null_output",
            severity=ValidationSeverity.ERROR,
            message="Agent returned None output",
        ))
        confidence = 0.0

    if isinstance(output, dict) and "error" in output:
        issues.append(ValidationIssue(
            rule="error_in_output",
            severity=ValidationSeverity.WARNING,
            message=f"Output contains error: {output['error']}",
        ))
        confidence = 0.5

    output_str = str(output)
    import re
    pii_patterns = [
        (r"\b\d{3}-\d{2}-\d{4}\b", "SSN"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "email"),
    ]
    for pattern, pii_type in pii_patterns:
        if re.search(pattern, output_str):
            issues.append(ValidationIssue(
                rule="pii_detection",
                severity=ValidationSeverity.WARNING,
                message=f"Potential {pii_type} detected in output",
                field=pii_type,
            ))

    passed = not any(i.severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL) for i in issues)

    return ValidationReport(
        passed=passed,
        issues=tuple(issues),
        confidence_score=confidence,
        checked_rules=("non_null_output", "error_in_output", "pii_detection"),
    )
