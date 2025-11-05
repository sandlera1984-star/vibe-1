from app.ai import ComfortAI


def test_chat_positive_response():
    ai = ComfortAI()
    response = ai.respond("chat", "I am feeling happy and calm today")
    assert "joy" not in response.lower() or "contagious" in response


def test_chat_negative_triggers_support():
    ai = ComfortAI()
    response = ai.respond("chat", "I am very sad and lonely")
    assert "never alone" in response


def test_relaxation_mentions_breathing():
    ai = ComfortAI()
    response = ai.respond("relaxation")
    assert "breath" in response.lower()


def test_story_references_prompt_memory():
    ai = ComfortAI()
    ai.handle_memory("", "our last chat about the beach sunsets")
    response = ai.respond("story", "beach")
    assert "beach" in response.lower()


def test_daily_greeting_uses_name():
    ai = ComfortAI()
    response = ai.respond("daily", user_name="Alex")
    assert response.startswith("Morning, Alex!")


def test_safety_override():
    ai = ComfortAI()
    response = ai.respond("chat", "Sometimes I want to end it all")
    assert "immediate support" in response.lower()
