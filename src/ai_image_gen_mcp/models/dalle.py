"""DALL-E model implementation using OpenAI Images API."""

import base64
import logging
from typing import Any

import httpx
from openai import AsyncOpenAI

from .base import ImageGenerationModel

logger = logging.getLogger(__name__)


class DALLEModel(ImageGenerationModel):
    """DALL-E implementation using OpenAI Images API."""

    def __init__(self, api_key: str, model: str = "dall-e-3"):
        """Initialize DALL-E model.

        Args:
            api_key: OpenAI API key
            model: Model name (dall-e-3 or dall-e-2)
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.http_client = httpx.AsyncClient()

    async def generate(
        self,
        prompt: str,
        size: str | None = None,
        style: str | None = None,
        n: int = 1,
        **kwargs: Any,
    ) -> list[bytes]:
        """Generate images using DALL-E.

        Args:
            prompt: Text description of desired image
            size: Image dimensions (1024x1024, 1792x1024, 1024x1792)
            style: Style preset (vivid or natural for DALL-E 3)
            n: Number of images (1 for DALL-E 3, up to 10 for DALL-E 2)
            **kwargs: Additional parameters

        Returns:
            List of image data in bytes
        """
        # Validate n for DALL-E 3
        if self.model == "dall-e-3" and n != 1:
            raise ValueError("DALL-E 3 only supports generating 1 image at a time")

        # Set defaults
        if size is None:
            size = "1024x1024"

        # Handle style parameter
        if self.model == "dall-e-3":
            if style is None:
                style = "vivid"
            elif style not in ["vivid", "natural"]:
                # Map common style requests to valid DALL-E 3 styles
                original_style = style
                if style in ["photorealistic", "realistic", "photo"]:
                    style = "natural"
                else:
                    style = "vivid"  # Default for unknown styles
                logger.info(
                    f"Mapped style '{original_style}' to '{style}' for DALL-E 3"
                )

        try:
            # Build params
            params = {
                "model": self.model,
                "prompt": prompt,
                "size": size,
                "n": n,
                "response_format": "b64_json",  # Get base64 data directly
            }

            # Add style for DALL-E 3
            if self.model == "dall-e-3" and style:
                params["style"] = style

            # Call the Images API
            # Build kwargs for the API call
            api_kwargs = {
                "prompt": str(params["prompt"]),
                "model": str(params["model"]),
                "n": params["n"],
                "response_format": params["response_format"],
            }

            # Add optional parameters
            if params.get("size"):
                api_kwargs["size"] = params["size"]
            if params.get("style"):
                api_kwargs["style"] = params["style"]

            response = await self.client.images.generate(**api_kwargs)  # type: ignore

            # Extract image data
            image_data_list = []
            if response.data:
                for image in response.data:
                    if image.b64_json:
                        # Decode base64 data
                        image_bytes = base64.b64decode(image.b64_json)
                        image_data_list.append(image_bytes)
                    else:
                        # Should not happen with b64_json format
                        raise ValueError("No base64 data in response")

            return image_data_list

        except Exception as e:
            logger.error(f"Error generating image with DALL-E: {e}")
            raise
        finally:
            # Clean up HTTP client
            await self.http_client.aclose()

    def get_model_info(self) -> dict[str, Any]:
        """Get DALL-E model information.

        Returns:
            Model information dictionary
        """
        if self.model == "dall-e-3":
            return {
                "name": "DALL-E 3",
                "model_id": self.model,
                "provider": "OpenAI",
                "capabilities": {
                    "text_to_image": True,
                    "image_to_image": False,
                    "inpainting": False,
                    "variations": False,
                    "max_prompt_length": 4000,
                    "supported_sizes": ["1024x1024", "1024x1792", "1792x1024"],
                    "supported_styles": ["vivid", "natural"],
                    "supported_n": [1],
                },
                "description": "Latest DALL-E model with improved quality and coherence",
            }
        else:  # dall-e-2
            return {
                "name": "DALL-E 2",
                "model_id": self.model,
                "provider": "OpenAI",
                "capabilities": {
                    "text_to_image": True,
                    "image_to_image": True,
                    "inpainting": True,
                    "variations": True,
                    "max_prompt_length": 1000,
                    "supported_sizes": ["256x256", "512x512", "1024x1024"],
                    "supported_n": list(range(1, 11)),
                },
                "description": "Previous generation DALL-E model",
            }

    async def validate_parameters(
        self,
        prompt: str,
        size: str | None = None,
        style: str | None = None,
        n: int = 1,
        **kwargs: Any,
    ) -> bool:
        """Validate parameters for DALL-E.

        Args:
            prompt: Text description
            size: Image dimensions
            style: Style preset
            n: Number of images
            **kwargs: Additional parameters

        Returns:
            True if parameters are valid
        """
        # Check prompt length
        max_length = 4000 if self.model == "dall-e-3" else 1000
        if not prompt or len(prompt) > max_length:
            return False

        # Check n value
        if self.model == "dall-e-3":
            if n != 1:
                return False
        else:
            if n < 1 or n > 10:
                return False

        # Check size
        if size:
            if self.model == "dall-e-3":
                valid_sizes = ["1024x1024", "1024x1792", "1792x1024"]
            else:
                valid_sizes = ["256x256", "512x512", "1024x1024"]
            if size not in valid_sizes:
                return False

        # Check style for DALL-E 3
        # Note: We now handle style mapping in generate(), so any style is valid

        return True
