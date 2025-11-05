"""Lightweight keyword-based safety monitor."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class SafetyConfig:
    crisis_keywords: tuple[str, ...] = (
        "suicide",
        "kill myself",
        "end it all",
        "self-harm",
        "hurt myself",
        "can't go on",
        "want to die",
    )


class SafetyMonitor:
    """Detect if a message suggests the user might need human support."""

    def __init__(self, config: SafetyConfig | None = None) -> None:
        self.config = config or SafetyConfig()

    def check(self, message: str) -> bool:
        lowered = message.lower()
        return any(keyword in lowered for keyword in self.config.crisis_keywords)

    def extend(self, keywords: Iterable[str]) -> None:
        unique = tuple(dict.fromkeys(self.config.crisis_keywords + tuple(keywords)))
        self.config.crisis_keywords = unique
