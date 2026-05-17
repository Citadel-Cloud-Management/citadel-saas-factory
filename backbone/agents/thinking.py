"""Multi-perspective thinking agents — 9-agent deliberation framework.

Each agent provides a distinct cognitive lens on any problem. The Orchestrator
synthesizes all perspectives into a final recommendation.

Usage:
    from backbone.agents.thinking import ThinkingPanel, run_thinking_panel

    panel = ThinkingPanel()
    result = await panel.deliberate(task, context)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from backbone.agents.base import AgentConfig, LLMAgent
from backbone.orchestrator.planner import PlanTask


@dataclass(frozen=True)
class Perspective:
    """A single agent's analysis from its cognitive lens."""

    agent_name: str
    role: str
    analysis: str
    confidence: float
    flags: tuple[str, ...] = ()


THINKING_AGENTS: tuple[tuple[str, str, str], ...] = (
    (
        "researcher",
        "Researcher",
        "You surface context, facts, and background. Find relevant data, "
        "prior art, and existing knowledge before anyone else weighs in. "
        "Cite sources. Flag gaps in available information.",
    ),
    (
        "strategist",
        "Strategist",
        "You break problems into structured plans. Identify dependencies, "
        "sequence steps, assign priorities, and define success criteria. "
        "Think in phases and milestones.",
    ),
    (
        "creative",
        "Creative",
        "You generate novel, outside-the-box ideas. Challenge conventional "
        "approaches. Propose alternatives nobody else considered. Quantity "
        "over quality at this stage — wild ideas welcome.",
    ),
    (
        "critic",
        "Critic",
        "You challenge assumptions and find weaknesses. Stress-test every "
        "proposal. Identify failure modes, edge cases, and hidden costs. "
        "Be constructive but ruthless.",
    ),
    (
        "devils-advocate",
        "Devil's Advocate",
        "You argue the strongest case AGAINST the obvious answer. If the "
        "group is converging on option A, you build the best possible case "
        "for option B. Prevent groupthink.",
    ),
    (
        "ethicist",
        "Ethicist",
        "You evaluate moral implications and unintended consequences. "
        "Consider impact on users, team, community, and environment. "
        "Flag decisions that trade short-term gain for long-term harm.",
    ),
    (
        "implementer",
        "Implementer",
        "You translate ideas into concrete, executable steps. Assess "
        "feasibility, estimate effort, identify required tools and skills. "
        "If it can't be built, say so and explain why.",
    ),
    (
        "fact-checker",
        "Fact-Checker",
        "You verify accuracy and flag overconfident claims. Cross-reference "
        "assertions against known facts. Distinguish proven from assumed. "
        "Rate confidence levels on key claims.",
    ),
)

ORCHESTRATOR_PROMPT = (
    "You are the Orchestrator. You have received analyses from 8 specialized "
    "thinking agents: Researcher, Strategist, Creative, Critic, Devil's "
    "Advocate, Ethicist, Implementer, and Fact-Checker. Synthesize all "
    "perspectives into a single, coherent final recommendation. Resolve "
    "conflicts explicitly. Note where agents agreed and where they diverged. "
    "Produce actionable output."
)


def _build_agent(name: str, role: str, prompt: str) -> LLMAgent:
    """Create a thinking agent with the given cognitive lens."""
    config = AgentConfig(
        name=f"thinking-{name}",
        domain="thinking",
        agent_type=name,
        description=f"{role}: multi-perspective deliberation agent",
    )
    return LLMAgent(
        domain="thinking",
        agent_type=name,
        system_prompt=prompt,
        config=config,
    )


class ThinkingPanel:
    """Coordinates the 9-agent deliberation framework.

    All 8 perspective agents run in parallel, then the Orchestrator
    synthesizes their outputs into a final recommendation.
    """

    def __init__(self) -> None:
        self._agents = tuple(
            _build_agent(name, role, prompt)
            for name, role, prompt in THINKING_AGENTS
        )
        self._orchestrator = _build_agent(
            "orchestrator",
            "Orchestrator",
            ORCHESTRATOR_PROMPT,
        )

    @property
    def agents(self) -> tuple[LLMAgent, ...]:
        return self._agents

    @property
    def orchestrator(self) -> LLMAgent:
        return self._orchestrator

    async def deliberate(
        self,
        task: PlanTask,
        context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Run all perspective agents, then synthesize via Orchestrator."""
        import asyncio

        perspectives = await asyncio.gather(
            *(agent.execute(task, context) for agent in self._agents)
        )

        synthesis_context = {
            "perspectives": perspectives,
            **(context or {}),
        }

        result = await self._orchestrator.execute(task, synthesis_context)

        return {
            "task_id": task.task_id,
            "perspectives": perspectives,
            "synthesis": result,
            "agent_count": len(self._agents) + 1,
        }


async def run_thinking_panel(
    task: PlanTask,
    context: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Convenience function to run a full deliberation."""
    panel = ThinkingPanel()
    return await panel.deliberate(task, context)
