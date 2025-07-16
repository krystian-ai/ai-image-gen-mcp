"""Storage module for AI Image Generation MCP Server."""

from .base import StorageBackend
from .local import LocalStorage

__all__ = ["StorageBackend", "LocalStorage"]