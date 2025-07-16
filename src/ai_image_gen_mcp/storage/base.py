"""Base storage interface for AI Image Generation MCP Server."""

from abc import ABC, abstractmethod


class StorageBackend(ABC):
    """Abstract base class for storage backends."""

    @abstractmethod
    async def save(self, data: bytes, filename: str, metadata: dict | None = None) -> str:
        """Save image data and return accessible URL/path.

        Args:
            data: Image data in bytes
            filename: Suggested filename
            metadata: Optional metadata to store with the image

        Returns:
            URL or path to access the saved image
        """
        pass

    @abstractmethod
    async def get(self, identifier: str) -> bytes:
        """Retrieve image data by identifier.

        Args:
            identifier: URL or path returned by save()

        Returns:
            Image data in bytes
        """
        pass

    @abstractmethod
    async def delete(self, identifier: str) -> bool:
        """Delete image by identifier.

        Args:
            identifier: URL or path returned by save()

        Returns:
            True if deleted successfully, False otherwise
        """
        pass

    @abstractmethod
    async def exists(self, identifier: str) -> bool:
        """Check if image exists.

        Args:
            identifier: URL or path returned by save()

        Returns:
            True if exists, False otherwise
        """
        pass
