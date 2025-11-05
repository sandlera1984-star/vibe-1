"""Simple in-memory store for user facts with keyword-based recall."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List


def _tokenise(text: str) -> List[str]:
    return [token.lower() for token in text.split()]


@dataclass
class MemoryItem:
    """Represents a fact the AI has learned about the user."""

    fact: str
    tokens: List[str] = field(init=False)

    def __post_init__(self) -> None:
        self.tokens = _tokenise(self.fact)


class UserMemory:
    """Stores short user facts and retrieves those relevant to a prompt."""

    def __init__(self) -> None:
        self._items: List[MemoryItem] = []

    def remember(self, fact: str) -> None:
        """Persist a new fact if it does not already exist."""

        fact = fact.strip()
        if not fact:
            return
        if any(item.fact.lower() == fact.lower() for item in self._items):
            return
        self._items.append(MemoryItem(fact))

    def recall(self, prompt: str, limit: int = 2) -> List[str]:
        """Return up to ``limit`` facts with shared keywords."""

        prompt_tokens = set(_tokenise(prompt))
        scored: List[tuple[int, MemoryItem]] = []
        for item in self._items:
            overlap = len(prompt_tokens.intersection(item.tokens))
            if overlap:
                scored.append((overlap, item))
        scored.sort(key=lambda pair: pair[0], reverse=True)
        return [item.fact for _, item in scored[:limit]]

    def dump(self) -> Iterable[str]:
        """Expose stored facts for persistence layers or testing."""

        return (item.fact for item in self._items)
