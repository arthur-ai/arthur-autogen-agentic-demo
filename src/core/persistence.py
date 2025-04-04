"""
Core persistence module for storing application state.

This module provides persistence functionality for storing and retrieving
application state data. Currently implements a simple in-memory store for
development and testing purposes.

Key Components:
- MockPersistence: Basic in-memory persistence implementation
- State management utilities
- Content storage and retrieval

Note: The current implementation is for development only. Production deployments
should use a proper database solution.
"""

from collections.abc import Mapping
from typing import Any

from src.utils.logger import get_logger


logger = get_logger(__name__)


class MockPersistence:
    """
    Simple in-memory persistence layer for storing and retrieving state.

    This class provides a basic implementation for development and testing.
    In production, this should be replaced with a proper database solution.

    Attributes:
        _content (Mapping[str, Any]): In-memory dictionary storing state data

    Note: This is not suitable for production use as data is lost when the
    process terminates.
    """

    def __init__(self):
        logger.debug("[MockPersistence.init] Initializing in-memory persistence")
        self._content: Mapping[str, Any] = {}

    def load_content(self) -> Mapping[str, Any]:
        """Retrieves stored content from memory"""
        logger.debug("[MockPersistence.load_content] Loading stored content")
        return self._content

    def save_content(self, content: Mapping[str, Any]) -> None:
        """Saves content to memory

        Args:
            content: Dictionary of data to persist
        """
        logger.debug("[MockPersistence.save_content] Saving content to memory")
        self._content = content
