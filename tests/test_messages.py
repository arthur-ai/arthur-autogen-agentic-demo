import pytest
from src.core.messages import AssistantTextMessage, UserTextMessage


def test_assistant_text_message():
    content = "Hello, how can I help?"
    source = "Assistant"
    message = AssistantTextMessage(content=content, source=source)

    assert message.content == content
    assert message.source == source


def test_user_text_message():
    content = "What's the stock price?"
    source = "User"
    message = UserTextMessage(content=content, source=source)

    assert message.content == content
    assert message.source == source


def test_message_equality():
    msg1 = UserTextMessage(content="test", source="User")
    msg2 = UserTextMessage(content="test", source="User")
    msg3 = UserTextMessage(content="different", source="User")

    assert msg1 == msg2
    assert msg1 != msg3


def test_message_string_representation():
    content = "test message"
    source = "User"
    message = UserTextMessage(content=content, source=source)

    # Get the actual string representation
    actual_str = str(message)
    # Verify it contains the essential components
    assert content in actual_str
    assert source in actual_str
    assert "UserTextMessage" in actual_str
