"""Base model interface for image generation."""

from abc import ABC, abstractmethod
from typing import Any


class ImageGenerationModel(ABC):
    """Abstract base class for image generation models."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        size: str | None = None,
        style: str | None = None,
        n: int = 1,
        **kwargs,
    ) -> list[bytes]:
        """Generate images based on prompt.

        Args:
            prompt: Text description of desired image
            size: Image dimensions
            style: Style preset
            n: Number of images to generate
            **kwargs: Additional model-specific parameters

        Returns:
            List of image data in bytes
        """
        pass

    @abstractmethod
    def get_model_info(self) -> dict[str, Any]:
        """Get model information.

        Returns:
            Dictionary containing model name, version, capabilities, etc.
        """
        pass

    @abstractmethod
    async def validate_parameters(
        self,
        prompt: str,
        size: str | None = None,
        style: str | None = None,
        n: int = 1,
        **kwargs,
    ) -> bool:
        """Validate generation parameters for this model.

        Args:
            prompt: Text description
            size: Image dimensions
            style: Style preset
            n: Number of images
            **kwargs: Additional parameters

        Returns:
            True if parameters are valid
        """
        pass
