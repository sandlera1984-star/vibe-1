"""Command-line interface for the comfort AI prototype."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict

from .ai import ComfortAI


@dataclass
class Command:
    description: str
    handler: Callable[[ComfortAI], None]


def _chat(ai: ComfortAI) -> None:
    print("Type 'quit' to return to the main menu.\n")
    while True:
        message = input("You: ")
        if message.strip().lower() in {"quit", "exit"}:
            break
        response = ai.respond("chat", message)
        print(f"{ai.config.persona_name}: {response}\n")


def _remember(ai: ComfortAI) -> None:
    fact = input("Tell me something you'd like me to remember: ")
    ai.handle_memory("", fact)
    print("Noted! I'll weave that into our chats when it fits.\n")


def _relax(ai: ComfortAI) -> None:
    print(f"{ai.config.persona_name}: {ai.respond('relaxation')}\n")


def _story(ai: ComfortAI) -> None:
    prompt = input("Share a theme or idea for today's mini adventure: ")
    print(f"{ai.config.persona_name}: {ai.respond('story', prompt)}\n")


def _daily(ai: ComfortAI) -> None:
    name = input("How should I address you today? (Leave blank for a surprise): ")
    print(f"{ai.config.persona_name}: {ai.respond('daily', user_name=name or None)}\n")


def _persona(ai: ComfortAI) -> None:
    print(ai.persona())
    print("\nKeywords that trigger safety escalations: " + ", ".join(ai.safety_keywords()) + "\n")


COMMANDS: Dict[str, Command] = {
    "1": Command("Chat with the AI", _chat),
    "2": Command("Teach the AI something about you", _remember),
    "3": Command("Start a guided relaxation", _relax),
    "4": Command("Play with a story prompt", _story),
    "5": Command("Receive a daily boost", _daily),
    "6": Command("View persona & safety info", _persona),
    "q": Command("Quit", lambda _: None),
}


def run() -> None:
    ai = ComfortAI()
    print(ai.persona())
    while True:
        print("\nSelect an option:")
        for key, command in COMMANDS.items():
            print(f"  {key}. {command.description}")
        choice = input("\nYour choice: ").strip().lower()
        if choice == "q":
            print("\nSending you off with a smile. Take good care!\n")
            return
        command = COMMANDS.get(choice)
        if not command:
            print("Let's try that again — please choose a valid option.\n")
            continue
        command.handler(ai)


if __name__ == "__main__":
    run()
