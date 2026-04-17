"""Compliance Scanner — automated compliance checking for the Citadel SaaS Factory.

Usage:
    python compliance/automation/scanner.py
    python compliance/automation/scanner.py --framework soc2
    python compliance/automation/scanner.py --report
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Finding:
    """Immutable compliance finding."""

    framework: str
    control_id: str
    severity: str  # pass, warning, fail, critical
    message: str
    evidence_path: str = ""
    remediation: str = ""


@dataclass(frozen=True)
class ScanResult:
    """Immutable scan result."""

    timestamp: str
    frameworks_scanned: tuple[str, ...]
    total_controls: int
    passed: int
    warnings: int
    failures: int
    findings: tuple[Finding, ...] = field(default_factory=tuple)


def scan_secrets_in_code(repo_root: Path) -> list[Finding]:
    """Check for hardcoded secrets in source code."""
    findings: list[Finding] = []
    secret_patterns = [
        ("password", "Hardcoded password"),
        ("api_key", "Hardcoded API key"),
        ("secret_key", "Hardcoded secret key"),
        ("private_key", "Hardcoded private key"),
        ("aws_access_key", "Hardcoded AWS key"),
    ]

    for py_file in repo_root.rglob("*.py"):
        if ".venv" in str(py_file) or "node_modules" in str(py_file):
            continue
        try:
            content = py_file.read_text(errors="ignore").lower()
            for pattern, desc in secret_patterns:
                for i, line in enumerate(content.split("\n"), 1):
                    if pattern in line and ("=" in line or ":" in line) and "os.getenv" not in line and "os.environ" not in line and "#" not in line.split(pattern)[0]:
                        if any(q in line for q in ['"sk-', "'sk-", '"AKIA', "'AKIA", "password123", "secretkey"]):
                            findings.append(Finding(
                                framework="soc2",
                                control_id="CC6.1",
                                severity="critical",
                                message=f"{desc} in {py_file.relative_to(repo_root)}:{i}",
                                evidence_path=str(py_file.relative_to(repo_root)),
                                remediation="Move secret to environment variable or Vault",
                            ))
        except Exception:
            pass

    return findings


def scan_env_files(repo_root: Path) -> list[Finding]:
    """Check for committed .env files."""
    findings: list[Finding] = []
    for env_file in repo_root.rglob(".env"):
        if ".git" in str(env_file):
            continue
        findings.append(Finding(
            framework="soc2",
            control_id="CC6.1",
            severity="warning",
            message=f".env file found: {env_file.relative_to(repo_root)}",
            evidence_path=str(env_file.relative_to(repo_root)),
            remediation="Ensure .env is in .gitignore and never committed",
        ))
    return findings


def scan_security_headers(repo_root: Path) -> list[Finding]:
    """Check that security headers middleware exists."""
    findings: list[Finding] = []
    headers_file = repo_root / "backend" / "app" / "middleware" / "security_headers.py"
    if not headers_file.exists():
        findings.append(Finding(
            framework="owasp",
            control_id="A05",
            severity="fail",
            message="Security headers middleware not found",
            remediation="Create backend/app/middleware/security_headers.py",
        ))
    return findings


def scan_rate_limiting(repo_root: Path) -> list[Finding]:
    """Check that rate limiting is implemented."""
    findings: list[Finding] = []
    rate_limit_file = repo_root / "backend" / "app" / "middleware" / "rate_limit.py"
    if rate_limit_file.exists():
        content = rate_limit_file.read_text()
        if "TODO" in content:
            findings.append(Finding(
                framework="owasp",
                control_id="A01",
                severity="fail",
                message="Rate limiting has unresolved TODOs",
                remediation="Implement Redis-based rate limiting",
            ))
    else:
        findings.append(Finding(
            framework="owasp",
            control_id="A01",
            severity="fail",
            message="Rate limiting middleware not found",
            remediation="Create backend/app/middleware/rate_limit.py",
        ))
    return findings


def scan_auth_middleware(repo_root: Path) -> list[Finding]:
    """Check that authentication is properly implemented."""
    findings: list[Finding] = []
    auth_file = repo_root / "backend" / "app" / "middleware" / "auth.py"
    if auth_file.exists():
        content = auth_file.read_text()
        if "TODO" in content:
            findings.append(Finding(
                framework="soc2",
                control_id="CC6.1",
                severity="fail",
                message="JWT authentication has unresolved TODOs",
                remediation="Implement JWT validation against Keycloak JWKS",
            ))
    return findings


def scan_guardrails(repo_root: Path) -> list[Finding]:
    """Check that guardrails are configured for LLM calls."""
    findings: list[Finding] = []
    guardrails_file = repo_root / "backend" / "app" / "middleware" / "guardrails.py"
    if not guardrails_file.exists():
        findings.append(Finding(
            framework="nist_ai",
            control_id="MANAGE-1",
            severity="critical",
            message="Guardrails middleware not found — LLM outputs unvalidated",
            remediation="Create backend/app/middleware/guardrails.py",
        ))
    return findings


def scan_encryption(repo_root: Path) -> list[Finding]:
    """Check for encryption configuration."""
    findings: list[Finding] = []
    headers_file = repo_root / "backend" / "app" / "middleware" / "security_headers.py"
    if headers_file.exists():
        content = headers_file.read_text()
        if "Strict-Transport-Security" not in content:
            findings.append(Finding(
                framework="pci_dss",
                control_id="req4",
                severity="warning",
                message="HSTS header not configured",
                remediation="Add Strict-Transport-Security header",
            ))
    return findings


def scan_all(repo_root: Path, framework_filter: str | None = None) -> ScanResult:
    """Run all compliance scans."""
    all_findings: list[Finding] = []

    scanners = [
        scan_secrets_in_code,
        scan_env_files,
        scan_security_headers,
        scan_rate_limiting,
        scan_auth_middleware,
        scan_guardrails,
        scan_encryption,
    ]

    for scanner in scanners:
        all_findings.extend(scanner(repo_root))

    if framework_filter:
        all_findings = [f for f in all_findings if f.framework == framework_filter]

    passed = sum(1 for f in all_findings if f.severity == "pass")
    warnings = sum(1 for f in all_findings if f.severity == "warning")
    failures = sum(1 for f in all_findings if f.severity in ("fail", "critical"))

    frameworks = tuple(sorted({f.framework for f in all_findings})) if all_findings else ("all",)

    return ScanResult(
        timestamp=datetime.now(timezone.utc).isoformat(),
        frameworks_scanned=frameworks,
        total_controls=len(all_findings),
        passed=passed,
        warnings=warnings,
        failures=failures,
        findings=tuple(all_findings),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Compliance Scanner")
    parser.add_argument("--framework", help="Scan specific framework")
    parser.add_argument("--report", action="store_true", help="Generate JSON report")
    parser.add_argument("--root", default=".", help="Repository root path")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    result = scan_all(repo_root, args.framework)

    if args.report:
        report = {
            "timestamp": result.timestamp,
            "frameworks": list(result.frameworks_scanned),
            "summary": {
                "total": result.total_controls,
                "passed": result.passed,
                "warnings": result.warnings,
                "failures": result.failures,
            },
            "findings": [
                {
                    "framework": f.framework,
                    "control_id": f.control_id,
                    "severity": f.severity,
                    "message": f.message,
                    "evidence_path": f.evidence_path,
                    "remediation": f.remediation,
                }
                for f in result.findings
            ],
        }
        print(json.dumps(report, indent=2))
    else:
        print(f"Compliance Scan — {result.timestamp}")
        print(f"Frameworks: {', '.join(result.frameworks_scanned)}")
        print(f"Results: {result.passed} passed, {result.warnings} warnings, {result.failures} failures")
        print()
        for f in result.findings:
            icon = {"pass": "[OK]", "warning": "[WARN]", "fail": "[FAIL]", "critical": "[CRIT]"}.get(f.severity, "[?]")
            print(f"  {icon} [{f.framework}:{f.control_id}] {f.message}")
            if f.remediation:
                print(f"       Fix: {f.remediation}")

    sys.exit(1 if result.failures > 0 else 0)


if __name__ == "__main__":
    main()
