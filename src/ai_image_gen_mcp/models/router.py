"""Model router for selecting and managing different image generation models."""

import logging
from typing import Any

from .base import ImageGenerationModel
from .dalle import DALLEModel
from .gpt_image import GPTImageModel

logger = logging.getLogger(__name__)


class ModelRouter:
    """Routes requests to appropriate image generation models."""

    def __init__(self) -> None:
        """Initialize model router."""
        self.models: dict[str, ImageGenerationModel] = {}
        self.default_model: str | None = None

    def register_model(
        self, name: str, model: ImageGenerationModel, is_default: bool = False
    ) -> None:
        """Register a model with the router.

        Args:
            name: Model identifier
            model: Model instance
            is_default: Whether this should be the default model
        """
        self.models[name] = model
        if is_default or self.default_model is None:
            self.default_model = name

        logger.info(f"Registered model: {name} (default: {is_default})")

    def get_model(self, name: str | None = None) -> ImageGenerationModel:
        """Get a model by name or return default.

        Args:
            name: Model name (optional)

        Returns:
            Model instance

        Raises:
            ValueError: If model not found
        """
        if name is None:
            name = self.default_model

        if name not in self.models:
            raise ValueError(
                f"Model '{name}' not found. Available: {list(self.models.keys())}"
            )

        return self.models[name]

    def list_models(self) -> list[dict[str, Any]]:
        """List all available models with their info.

        Returns:
            List of model information dictionaries
        """
        return [
            {
                "id": name,
                "is_default": name == self.default_model,
                **model.get_model_info(),
            }
            for name, model in self.models.items()
        ]

    @classmethod
    def create_default_router(cls, config: Any) -> "ModelRouter":
        """Create router with default model configuration.

        Args:
            config: Server configuration

        Returns:
            Configured ModelRouter instance
        """
        router = cls()

        # Register models based on provider
        if config.model_provider == "openai" and config.openai_api_key:
            # Register DALL-E models
            dalle3 = DALLEModel(api_key=config.openai_api_key, model="dall-e-3")
            router.register_model("dalle-3", dalle3, is_default=True)

            dalle2 = DALLEModel(api_key=config.openai_api_key, model="dall-e-2")
            router.register_model("dalle-2", dalle2)

            # Register GPT-Image-1 (but not as default due to timeout issues)
            gpt_image = GPTImageModel(
                api_key=config.openai_api_key, model=config.model_default
            )
            router.register_model("gpt-image-1", gpt_image)

        return router
