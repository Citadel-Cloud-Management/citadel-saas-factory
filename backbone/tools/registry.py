"""Tool Registry — manages agent access to internal/external tools."""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Coroutine

import structlog

logger = structlog.get_logger("tools")


class ToolCategory(str, Enum):
    API = "api"
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    SEARCH = "search"
    MESSAGING = "messaging"
    CI_CD = "ci_cd"
    CLOUD = "cloud"
    BROWSER = "browser"
    TERMINAL = "terminal"


@dataclass(frozen=True)
class ToolConfig:
    """Immutable tool configuration."""

    name: str
    category: ToolCategory
    description: str = ""
    requires_auth: bool = False
    rate_limit_per_minute: int = 60
    timeout_seconds: int = 30
    allowed_domains: tuple[str, ...] = field(default_factory=tuple)
    risk_level: str = "low"


@dataclass
class ToolUsageRecord:
    """Mutable record of tool invocations for audit and rate limiting."""

    tool_name: str
    invocation_count: int = 0
    last_invoked: float = 0.0
    errors: int = 0
    total_latency_ms: float = 0.0


class ToolRegistry:
    """Manages tool registration, access control, rate limiting, and audit.

    Every tool has:
    - Authentication boundary
    - Rate limits
    - Retry logic
    - Action logging
    - Rollback plan (where possible)
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolConfig] = {}
        self._handlers: dict[str, Callable[..., Coroutine]] = {}
        self._usage: dict[str, ToolUsageRecord] = {}
        self._invocation_timestamps: dict[str, list[float]] = {}
        self._rbac: Any = None

    def register(
        self,
        config: ToolConfig,
        handler: Callable[..., Coroutine],
    ) -> None:
        """Register a tool with its handler."""
        self._tools[config.name] = config
        self._handlers[config.name] = handler
        self._usage[config.name] = ToolUsageRecord(tool_name=config.name)
        self._invocation_timestamps[config.name] = []
        logger.info("tool_registered", name=config.name, category=config.category.value)

    def set_rbac(self, rbac_manager: Any) -> None:
        """Attach an RBAC manager for access control enforcement."""
        self._rbac = rbac_manager

    async def invoke(
        self,
        tool_name: str,
        agent_domain: str,
        agent_id: str = "",
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Invoke a tool with RBAC, domain check, rate limiting, timeout, and audit."""
        config = self._tools.get(tool_name)
        if not config:
            raise ValueError(f"Tool not registered: {tool_name}")

        handler = self._handlers.get(tool_name)
        if not handler:
            raise ValueError(f"No handler for tool: {tool_name}")

        if config.allowed_domains and agent_domain not in config.allowed_domains:
            logger.warning(
                "tool_domain_denied",
                tool=tool_name,
                agent_domain=agent_domain,
                allowed=config.allowed_domains,
            )
            raise PermissionError(f"Domain {agent_domain} not allowed for tool {tool_name}")

        if config.requires_auth and self._rbac is not None:
            from backbone.governance.rbac import Permission
            decision = self._rbac.check_access(agent_id or agent_domain, tool_name, Permission.EXECUTE)
            if not decision.allowed:
                logger.warning("tool_rbac_denied", tool=tool_name, agent=agent_id, reason=decision.reason)
                raise PermissionError(f"RBAC denied: {decision.reason}")
        elif config.requires_auth:
            logger.warning("tool_auth_required_no_rbac", tool=tool_name)
            raise PermissionError(f"Tool {tool_name} requires auth but no RBAC manager configured")

        if not self._check_rate_limit(tool_name, config):
            raise RuntimeError(f"Rate limit exceeded for {tool_name}")

        usage = self._usage[tool_name]
        start = time.monotonic()

        try:
            result = await asyncio.wait_for(
                handler(**(params or {})),
                timeout=config.timeout_seconds,
            )
            elapsed = (time.monotonic() - start) * 1000
            usage.invocation_count += 1
            usage.last_invoked = time.time()
            usage.total_latency_ms += elapsed

            logger.info(
                "tool_invoked",
                tool=tool_name,
                agent_domain=agent_domain,
                latency_ms=round(elapsed, 2),
            )
            return result

        except asyncio.TimeoutError:
            usage.errors += 1
            logger.error("tool_timeout", tool=tool_name, timeout=config.timeout_seconds)
            raise
        except Exception as exc:
            usage.errors += 1
            logger.error("tool_error", tool=tool_name, error=str(exc))
            raise

    def _check_rate_limit(self, tool_name: str, config: ToolConfig) -> bool:
        """Sliding window rate limit check."""
        now = time.time()
        window_start = now - 60
        timestamps = self._invocation_timestamps[tool_name]

        self._invocation_timestamps[tool_name] = [t for t in timestamps if t > window_start]
        timestamps = self._invocation_timestamps[tool_name]

        if len(timestamps) >= config.rate_limit_per_minute:
            return False

        timestamps.append(now)
        return True

    def get_usage(self, tool_name: str) -> ToolUsageRecord | None:
        return self._usage.get(tool_name)

    def list_tools(self, category: ToolCategory | None = None) -> list[ToolConfig]:
        tools = list(self._tools.values())
        if category:
            tools = [t for t in tools if t.category == category]
        return tools
