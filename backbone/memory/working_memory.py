"""Layer 1: Working Memory — context window management.

Manages what goes into the LLM's context window for each call.
Handles token budgeting, priority-based truncation, and injection ordering.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Sequence

from backbone.memory.config import WorkingMemoryConfig
from backbone.memory.schemas import WorkingMemoryEntry


@dataclass
class WorkingMemoryState:
    """Mutable state for a single LLM call's context window."""

    entries: list[WorkingMemoryEntry] = field(default_factory=list)
    total_tokens: int = 0
    max_tokens: int = 128_000
    reserved_tokens: int = 4_096

    @property
    def available_tokens(self) -> int:
        return max(0, self.max_tokens - self.reserved_tokens - self.total_tokens)


class WorkingMemoryManager:
    """Manages the context window for a single LLM invocation.

    Responsibilities:
    - Token budget tracking
    - Priority-based message ordering
    - Truncation when budget exceeded
    - System prompt injection
    """

    def __init__(self, config: WorkingMemoryConfig) -> None:
        self._config = config

    def create_state(self) -> WorkingMemoryState:
        return WorkingMemoryState(
            max_tokens=self._config.max_tokens,
            reserved_tokens=self._config.reserved_tokens,
        )

    def add_entry(self, state: WorkingMemoryState, entry: WorkingMemoryEntry) -> WorkingMemoryState:
        """Add an entry to working memory. Returns new state (immutable pattern)."""
        new_entries = [*state.entries, entry]
        new_total = state.total_tokens + entry.token_count
        return WorkingMemoryState(
            entries=new_entries,
            total_tokens=new_total,
            max_tokens=state.max_tokens,
            reserved_tokens=state.reserved_tokens,
        )

    def truncate(self, state: WorkingMemoryState) -> WorkingMemoryState:
        """Truncate entries to fit within token budget.

        Strategy determined by config:
        - priority: drop lowest-priority entries first
        - fifo: drop oldest entries first
        - sliding_window: keep last N entries that fit
        """
        budget = state.max_tokens - state.reserved_tokens
        if state.total_tokens <= budget:
            return state

        if self._config.truncation_strategy == "priority":
            return self._truncate_by_priority(state, budget)
        elif self._config.truncation_strategy == "sliding_window":
            return self._truncate_sliding_window(state, budget)
        return self._truncate_fifo(state, budget)

    def build_messages(self, state: WorkingMemoryState) -> list[dict[str, str]]:
        """Convert working memory to LLM message format."""
        truncated = self.truncate(state)
        return [
            {"role": entry.role, "content": entry.content}
            for entry in truncated.entries
        ]

    def _truncate_by_priority(self, state: WorkingMemoryState, budget: int) -> WorkingMemoryState:
        sorted_entries = sorted(state.entries, key=lambda e: e.priority, reverse=True)
        kept: list[WorkingMemoryEntry] = []
        total = 0
        for entry in sorted_entries:
            if total + entry.token_count <= budget:
                kept.append(entry)
                total += entry.token_count
        # Restore original order
        original_order = {id(e): i for i, e in enumerate(state.entries)}
        kept.sort(key=lambda e: original_order.get(id(e), 0))
        return WorkingMemoryState(
            entries=kept, total_tokens=total,
            max_tokens=state.max_tokens, reserved_tokens=state.reserved_tokens,
        )

    def _truncate_fifo(self, state: WorkingMemoryState, budget: int) -> WorkingMemoryState:
        kept: list[WorkingMemoryEntry] = []
        total = 0
        for entry in reversed(state.entries):
            if total + entry.token_count <= budget:
                kept.insert(0, entry)
                total += entry.token_count
        return WorkingMemoryState(
            entries=kept, total_tokens=total,
            max_tokens=state.max_tokens, reserved_tokens=state.reserved_tokens,
        )

    def _truncate_sliding_window(self, state: WorkingMemoryState, budget: int) -> WorkingMemoryState:
        return self._truncate_fifo(state, budget)
