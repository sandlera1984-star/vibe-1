"""Heuristic sentiment analyser used to steer response tone."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SentimentLexicon:
    positives: tuple[str, ...]
    negatives: tuple[str, ...]


_DEFAULT_LEXICON = SentimentLexicon(
    positives=(
        "glad",
        "happy",
        "excited",
        "awesome",
        "great",
        "love",
        "joy",
        "calm",
        "peaceful",
    ),
    negatives=(
        "sad",
        "angry",
        "upset",
        "anxious",
        "worried",
        "lonely",
        "stressed",
        "tired",
        "hate",
    ),
)


class SentimentAnalyzer:
    """Return a sentiment score in the range ``[-1, 1]``."""

    def __init__(self, lexicon: SentimentLexicon | None = None) -> None:
        self.lexicon = lexicon or _DEFAULT_LEXICON

    def score(self, text: str) -> float:
        tokens = [token.strip(".,!?;:").lower() for token in text.split()]
        positives = sum(token in self.lexicon.positives for token in tokens)
        negatives = sum(token in self.lexicon.negatives for token in tokens)
        total = positives + negatives
        if total == 0:
            return 0.0
        return (positives - negatives) / total

    def tone(self, text: str) -> str:
        score = self.score(text)
        if score >= 0.2:
            return "positive"
        if score <= -0.2:
            return "negative"
        return "neutral"

    def learn(self, positive: Iterable[str] = (), negative: Iterable[str] = ()) -> None:
        """Extend the lexicon with user-provided vocabulary."""

        positives = tuple(dict.fromkeys(self.lexicon.positives + tuple(positive)))
        negatives = tuple(dict.fromkeys(self.lexicon.negatives + tuple(negative)))
        object.__setattr__(self.lexicon, "positives", positives)
        object.__setattr__(self.lexicon, "negatives", negatives)
