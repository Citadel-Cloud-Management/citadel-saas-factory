"""Base agent interface — all agents implement this contract."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from typing import Any

import structlog

from backbone.orchestrator.planner import PlanTask

logger = structlog.get_logger("agent")


@dataclass(frozen=True)
class AgentConfig:
    """Immutable agent configuration."""

    name: str
    domain: str
    agent_type: str
    description: str = ""
    allowed_tools: tuple[str, ...] = field(default_factory=tuple)
    max_retries: int = 3
    timeout_seconds: int = 300
    autonomy_level: int = 3


class BaseAgent(abc.ABC):
    """Abstract base for all agents in the backbone.

    Every agent must define:
    - domain: which business domain it belongs to
    - agent_type: its specific role
    - execute: how it processes a task
    """

    def __init__(self, domain: str, agent_type: str, config: AgentConfig | None = None) -> None:
        self._domain = domain
        self._agent_type = agent_type
        self._config = config or AgentConfig(
            name=f"{domain}-{agent_type}",
            domain=domain,
            agent_type=agent_type,
        )

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def agent_type(self) -> str:
        return self._agent_type

    @property
    def config(self) -> AgentConfig:
        return self._config

    @abc.abstractmethod
    async def execute(self, task: PlanTask, context: dict[str, Any] | None = None) -> Any:
        """Execute a task and return the result."""

    async def validate_input(self, task: PlanTask) -> bool:
        """Validate task input before execution. Override for custom validation."""
        return True

    async def validate_output(self, output: Any) -> bool:
        """Validate output after execution. Override for custom validation."""
        return True


class NoOpAgent(BaseAgent):
    """Fallback agent that logs a warning and returns empty result."""

    async def execute(self, task: PlanTask, context: dict[str, Any] | None = None) -> Any:
        logger.warning(
            "noop_agent_called",
            task_id=task.task_id,
            domain=self.domain,
            agent_type=self.agent_type,
        )
        return {"status": "no_agent_available", "task_id": task.task_id}


class LLMAgent(BaseAgent):
    """Agent that delegates work to an LLM with system prompt and tools.

    This is the primary agent type — wraps Claude/OpenAI/Ollama calls
    with the guardrails middleware.
    """

    def __init__(
        self,
        domain: str,
        agent_type: str,
        system_prompt: str,
        config: AgentConfig | None = None,
    ) -> None:
        super().__init__(domain, agent_type, config)
        self._system_prompt = system_prompt

    async def execute(self, task: PlanTask, context: dict[str, Any] | None = None) -> Any:
        """Execute task via LLM call with guardrails validation."""
        from backbone.validation.validator import validate_input, validate_output

        prompt = f"{self._system_prompt}\n\nTask: {task.description}"
        if context:
            prompt += f"\n\nContext: {_sanitize_context(context)}"

        input_report = await validate_input(prompt)
        if not input_report.passed:
            logger.warning(
                "llm_agent_input_rejected",
                domain=self.domain,
                task_id=task.task_id,
                issues=[i.message for i in input_report.issues],
            )
            return {
                "agent": f"{self.domain}:{self.agent_type}",
                "task_id": task.task_id,
                "status": "input_rejected",
                "validation": input_report,
            }

        logger.info(
            "llm_agent_execute",
            domain=self.domain,
            agent_type=self.agent_type,
            task_id=task.task_id,
        )

        # In production, this calls the actual LLM via guard_llm_call
        # For now, return structured placeholder showing the pipeline works
        raw_output = {
            "agent": f"{self.domain}:{self.agent_type}",
            "task_id": task.task_id,
            "task_name": task.name,
            "status": "executed",
            "prompt_length": len(prompt),
        }

        validation = await validate_output(raw_output, task)
        return {**raw_output, "validation": validation}


def _sanitize_context(context: dict[str, Any] | Any) -> str:
    """Flatten context to string, extracting all string leaves for validation."""
    if isinstance(context, str):
        return context
    if isinstance(context, dict):
        parts = []
        for k, v in context.items():
            parts.append(f"{k}: {_sanitize_context(v)}")
        return "; ".join(parts)
    if isinstance(context, (list, tuple)):
        return ", ".join(_sanitize_context(item) for item in context)
    return str(context)
