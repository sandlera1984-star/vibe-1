from app.memory import UserMemory


def test_remember_and_recall():
    memory = UserMemory()
    memory.remember("I love hiking in the mountains")
    memory.remember("My favourite drink is chai latte")

    results = memory.recall("Tell me about your favourite drink")
    assert "My favourite drink is chai latte" in results


def test_duplicate_facts_not_added():
    memory = UserMemory()
    memory.remember("I enjoy painting")
    memory.remember("I enjoy painting")

    assert list(memory.dump()) == ["I enjoy painting"]
