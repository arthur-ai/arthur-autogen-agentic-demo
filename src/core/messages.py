"""Message type definitions for the conversation system.

This module defines the core message classes used throughout the system for
communication between different components. It includes base message types
and specialized message classes for user interactions, assistant responses,
and system control.

Classes:
    TextMessage: Base class for all text-based messages
    GetSlowUserMessage: Message class for requesting user input
    TerminateMessage: Message class for conversation termination
    UserTextMessage: Specialized class for user messages
    AssistantTextMessage: Specialized class for assistant messages
"""

from dataclasses import dataclass


@dataclass
class TextMessage:
    """
    Base class for text-based messages in the system.

    Attributes:
        source (str): The origin/sender of the message (e.g., "user", "assistant", "system")
        content (str): The actual message content as plain text

    Note: This serves as the parent class for specialized message types like
    UserTextMessage and AssistantTextMessage.
    """

    source: str
    content: str


@dataclass
class GetSlowUserMessage:
    """
    Message class representing a request for user input.
    Used when the system needs to pause and wait for user interaction.

    Attributes:
        content (str): The message or prompt to show to the user
    """

    content: str


@dataclass
class TerminateMessage:
    """
    Message class indicating that the conversation should be terminated.
    Used for graceful shutdown or error conditions.

    Attributes:
        content (str): The reason or message for termination
    """

    content: str


@dataclass
class UserTextMessage(TextMessage):
    """
    Represents a message from the user in the conversation.
    Inherits from TextMessage and maintains the same structure.
    Used to differentiate user messages from other message types.
    """

    pass


@dataclass
class AssistantTextMessage(TextMessage):
    """
    Represents a message from the AI assistant in the conversation.
    Inherits from TextMessage and maintains the same structure.
    Used to differentiate assistant messages from other message types.
    """

    pass
