import pytest

from src.dialogues.messages_to_llm import MessagesToLlm


# Test: Adding a simple message with valid data
def test_add_message():
    messages = MessagesToLlm()
    messages.add_message(role="user", content="Hello")
    assert len(messages.get()) == 1
    assert messages.get()[0] == {"role": "user", "content": "Hello"}


# Test: Adding a system message replaces the previous system message
def test_system_message_replaces_first():
    messages = MessagesToLlm()
    messages.add_message(role="system", content="Initial system message")
    assert messages.get()[0] == {"role": "system", "content": "Initial system message"}

    messages.add_message(role="system", content="Updated system message")
    assert len(messages.get()) == 1  # System message should replace the first one
    assert messages.get()[0] == {"role": "system", "content": "Updated system message"}


# Test: Adding a message with an empty role or content raises an error
def test_add_message_empty_role_or_content():
    messages = MessagesToLlm()

    with pytest.raises(ValueError, match="role can't be empty."):
        messages.add_message(role="", content="Valid content")

    with pytest.raises(ValueError, match="content can't be empty."):
        messages.add_message(role="user", content="")


# Test: Guiding messages are correctly indexed
def test_add_guiding_message():
    messages = MessagesToLlm()
    messages.add_message(role="user", content="Normal message")
    messages.add_message(role="user", content="Guiding message", is_guiding_message=True)

    assert len(messages.get()) == 2
    assert messages.get_guiding_message_indices() == [1]  # Only the second message is guiding


# Test: Extending from another MessagesToLlm instance without user/assistant messages
def test_extend_from_empty_messages():
    messages1 = MessagesToLlm()
    messages1.add_message(role="user", content="Message 1")

    messages2 = MessagesToLlm()
    messages2.add_message(role="user", content="Message 2")

    messages1.extend_from_messages_to_llm(messages2)

    assert len(messages1.get()) == 2
    assert messages1.get()[1] == {"role": "user", "content": "Message 2"}


# Test: Extending with guiding messages is skipped when user/assistant messages exist
def test_extend_skips_guiding_messages():
    messages1 = MessagesToLlm()
    messages1.add_message(role="user", content="User message 1")

    messages2 = MessagesToLlm()
    messages2.add_message(role="user", content="Guiding message", is_guiding_message=True)
    messages2.add_message(role="assistant", content="Assistant message")

    messages1.extend_from_messages_to_llm(messages2)

    assert len(messages1.get()) == 2  # It should have all messages except the guiding one
    assert messages1.get()[1] == {"role": "assistant", "content": "Assistant message"}


# Test: Extending with guiding messages when no user/assistant messages exist
def test_extend_includes_guiding_messages_when_no_user_or_assistant():
    messages1 = MessagesToLlm()

    messages2 = MessagesToLlm()
    messages2.add_message(role="user", content="Guiding message", is_guiding_message=True)
    messages2.add_message(role="assistant", content="Assistant message")

    messages1.extend_from_messages_to_llm(messages2)

    assert len(messages1.get()) == 2  # Both messages should be included
    assert messages1.get()[0] == {"role": "user", "content": "Guiding message"}
    assert messages1.get()[1] == {"role": "assistant", "content": "Assistant message"}
