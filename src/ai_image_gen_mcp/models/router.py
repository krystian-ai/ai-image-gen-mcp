"""Model router for selecting and managing different image generation models."""

import logging
from typing import Dict, Optional, List
from .base import ImageGenerationModel
from .gpt_image import GPTImageModel


logger = logging.getLogger(__name__)


class ModelRouter:
    """Routes requests to appropriate image generation models."""
    
    def __init__(self):
        """Initialize model router."""
        self.models: Dict[str, ImageGenerationModel] = {}
        self.default_model: Optional[str] = None
    
    def register_model(self, name: str, model: ImageGenerationModel, is_default: bool = False):
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
    
    def get_model(self, name: Optional[str] = None) -> ImageGenerationModel:
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
            raise ValueError(f"Model '{name}' not found. Available: {list(self.models.keys())}")
        
        return self.models[name]
    
    def list_models(self) -> List[Dict[str, any]]:
        """List all available models with their info.
        
        Returns:
            List of model information dictionaries
        """
        return [
            {
                "id": name,
                "is_default": name == self.default_model,
                **model.get_model_info()
            }
            for name, model in self.models.items()
        ]
    
    @classmethod
    def create_default_router(cls, config) -> "ModelRouter":
        """Create router with default model configuration.
        
        Args:
            config: Server configuration
            
        Returns:
            Configured ModelRouter instance
        """
        router = cls()
        
        # Register GPT-Image-1
        if config.model_provider == "openai" and config.openai_api_key:
            gpt_image = GPTImageModel(
                api_key=config.openai_api_key,
                model=config.model_default
            )
            router.register_model("gpt-image-1", gpt_image, is_default=True)
        
        # Future: Add more models here
        # router.register_model("dalle-3", DallE3Model(...))
        # router.register_model("stable-diffusion", StableDiffusionModel(...))
        
        return router