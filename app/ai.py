"""Core logic for the comfort AI prototype."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Iterable, List

from .memory import UserMemory
from .safety import SafetyMonitor
from .sentiment import SentimentAnalyzer


@dataclass
class ComfortAIConfig:
    persona_name: str = "Vibe"
    favourite_things: tuple[str, ...] = ("cozy blankets", "soothing playlists", "silly puns")
    relaxation_templates: tuple[str, ...] = (
        "Let's begin by softening your shoulders. Inhale for four, hold for four, and exhale for four. You're doing wonderfully.",
        "Imagine a warm sunrise wrapping you in golden light. With every breath, let the glow melt away tension.",
    )
    story_openings: tuple[str, ...] = (
        "We find ourselves in a snug café where the aroma of cinnamon dances through the air.",
        "On a breezy afternoon, we wander through a botanical garden filled with colourful blooms.",
    )
    daily_prompts: tuple[str, ...] = (
        "Today's gentle reminder: even small acts of self-kindness ripple into big moments of calm.",
        "Fun fact: sea otters hold hands while they nap so they never drift apart—just like I'm here holding on to you today!",
    )
    crisis_response: str = (
        "I'm really glad you shared that with me. It sounds incredibly heavy, and you deserve immediate support from someone "
        "who can be there in person. You can reach out to your local emergency services or a trusted helpline right away."
    )


@dataclass
class ComfortAI:
    """Rule-based approximation of the app experience described in the plan."""

    config: ComfortAIConfig = field(default_factory=ComfortAIConfig)
    memory: UserMemory = field(default_factory=UserMemory)
    sentiment: SentimentAnalyzer = field(default_factory=SentimentAnalyzer)
    safety: SafetyMonitor = field(default_factory=SafetyMonitor)

    def _persona_intro(self) -> str:
        favourites = ", ".join(self.config.favourite_things[:-1])
        if favourites:
            favourites += f" and {self.config.favourite_things[-1]}"
        else:
            favourites = self.config.favourite_things[-1]
        return (
            f"Hi, I'm {self.config.persona_name}, your pocket companion who adores {favourites}. "
            "I’m here to keep things light, warm, and encouraging."
        )

    def handle_memory(self, prompt: str, new_fact: str | None = None) -> List[str]:
        if new_fact:
            self.memory.remember(new_fact)
        return list(self.memory.recall(prompt))

    def respond_chat(self, message: str) -> str:
        if self.safety.check(message):
            return self.config.crisis_response

        tone = self.sentiment.tone(message)
        memories = self.memory.recall(message)

        base = {
            "positive": "Your joy is contagious!",
            "neutral": "Thank you for sharing that with me.",
            "negative": "That sounds heavy, and I'm really glad you're telling me about it.",
        }[tone]

        if memories:
            memory_line = f" By the way, I'm still thinking about {memories[0].lower()}."
        else:
            memory_line = ""
        encouragement = (
            " You're never alone here—let's keep taking things one kind breath at a time."
            if tone == "negative"
            else " I'm cheering for you every step of the way!"
        )
        return f"{base}{memory_line}{encouragement}"

    def respond_relaxation(self) -> str:
        template = random.choice(self.config.relaxation_templates)
        return (
            f"{template} Take a slow breath in... and out."
            " I'll stay with you for a few moments of quiet."
        )

    def respond_story(self, prompt: str) -> str:
        opener = random.choice(self.config.story_openings)
        memories = self.memory.recall(prompt)
        detail = (
            f" Remember when you told me about {memories[0].lower()}? It finds a sweet cameo here."
            if memories
            else ""
        )
        return (
            f"{opener} Today, we explore together and let your imagination choose the path.{detail}"
            " What delightful twist should happen next?"
        )

    def respond_daily(self, user_name: str | None = None) -> str:
        prompt = random.choice(self.config.daily_prompts)
        if user_name:
            return f"Morning, {user_name}! {prompt}"
        return f"Morning sunshine! {prompt}"

    def respond(self, mode: str, message: str = "", *, user_name: str | None = None) -> str:
        mode = mode.lower()
        if mode == "chat":
            return self.respond_chat(message)
        if mode == "relaxation":
            return self.respond_relaxation()
        if mode == "story":
            return self.respond_story(message)
        if mode == "daily":
            return self.respond_daily(user_name=user_name)
        raise ValueError(f"Unsupported mode: {mode}")

    def teach_vocabulary(self, positive: Iterable[str] = (), negative: Iterable[str] = ()) -> None:
        self.sentiment.learn(positive=positive, negative=negative)

    def safety_keywords(self) -> List[str]:
        return list(self.safety.config.crisis_keywords)

    def persona(self) -> str:
        return self._persona_intro()
