"""Local filesystem storage backend."""

import hashlib
import json
from datetime import datetime
from pathlib import Path

import aiofiles
import aiofiles.os

from .base import StorageBackend


class LocalStorage(StorageBackend):
    """Local filesystem storage implementation."""

    def __init__(self, base_path: Path):
        """Initialize local storage.

        Args:
            base_path: Base directory for storing images
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, original_filename: str, data: bytes) -> str:
        """Generate unique filename based on content hash.

        Args:
            original_filename: Original filename suggestion
            data: Image data

        Returns:
            Unique filename
        """
        # Extract extension
        ext = Path(original_filename).suffix or ".png"

        # Generate hash of content
        content_hash = hashlib.sha256(data).hexdigest()[:12]

        # Create timestamp
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        # Combine for unique filename
        return f"{timestamp}_{content_hash}{ext}"

    async def save(self, data: bytes, filename: str, metadata: dict | None = None) -> str:
        """Save image data to local filesystem.

        Args:
            data: Image data in bytes
            filename: Suggested filename
            metadata: Optional metadata to store with the image

        Returns:
            Path to saved image
        """
        # Generate unique filename
        unique_filename = self._generate_filename(filename, data)
        file_path = self.base_path / unique_filename

        # Save image data
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(data)

        # Save metadata if provided
        if metadata:
            metadata_path = file_path.with_suffix(file_path.suffix + ".json")
            async with aiofiles.open(metadata_path, 'w') as f:
                await f.write(json.dumps(metadata, indent=2))

        # Return absolute path as string
        return str(file_path.absolute())

    async def get(self, identifier: str) -> bytes:
        """Retrieve image data from local filesystem.

        Args:
            identifier: File path

        Returns:
            Image data in bytes
        """
        file_path = Path(identifier)

        if not file_path.exists():
            raise FileNotFoundError(f"Image not found: {identifier}")

        async with aiofiles.open(file_path, 'rb') as f:
            return await f.read()

    async def delete(self, identifier: str) -> bool:
        """Delete image from local filesystem.

        Args:
            identifier: File path

        Returns:
            True if deleted successfully, False otherwise
        """
        file_path = Path(identifier)

        try:
            if file_path.exists():
                await aiofiles.os.remove(file_path)

                # Also remove metadata if exists
                metadata_path = file_path.with_suffix(file_path.suffix + ".json")
                if metadata_path.exists():
                    await aiofiles.os.remove(metadata_path)

                return True
            return False
        except Exception:
            return False

    async def exists(self, identifier: str) -> bool:
        """Check if image exists in local filesystem.

        Args:
            identifier: File path

        Returns:
            True if exists, False otherwise
        """
        return Path(identifier).exists()
