"""GPT-Image-1 model implementation using OpenAI Responses API."""

import base64
import logging
from typing import Any

from openai import AsyncOpenAI

from .base import ImageGenerationModel

logger = logging.getLogger(__name__)


class GPTImageModel(ImageGenerationModel):
    """GPT-Image-1 implementation using OpenAI Responses API."""

    def __init__(self, api_key: str, model: str = "gpt-4.1-mini"):
        """Initialize GPT-Image model.

        Args:
            api_key: OpenAI API key
            model: Model name (default: gpt-4.1-mini)
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model

    async def generate(
        self,
        prompt: str,
        size: str | None = None,
        style: str | None = None,
        n: int = 1,
        **kwargs,
    ) -> list[bytes]:
        """Generate images using GPT-Image-1.

        Args:
            prompt: Text description of desired image
            size: Image dimensions (not used for GPT-Image-1)
            style: Style preset (not used for GPT-Image-1)
            n: Number of images (must be 1 for GPT-Image-1)
            **kwargs: Additional parameters

        Returns:
            List of image data in bytes
        """
        # GPT-Image-1 only supports n=1
        if n != 1:
            raise ValueError("GPT-Image-1 only supports generating 1 image at a time")

        try:
            # Call the Responses API with image generation tool
            response = await self.client.responses.create(
                model=self.model,
                input=prompt,
                tools=[{"type": "image_generation"}],
                tool_choice={"type": "image_generation"},
            )

            # Extract image data from response
            if not response.output or len(response.output) == 0:
                raise ValueError("No output in response")

            # Get the image data from the first output
            # The output is an ImageGenerationCall with a result field containing base64 data
            first_output = response.output[0]
            if not hasattr(first_output, "result"):
                raise ValueError("No image result in response")

            image_outputs = [first_output.result]

            # Convert base64 to bytes
            image_data_list = []
            for base64_data in image_outputs:
                image_bytes = base64.b64decode(base64_data)
                image_data_list.append(image_bytes)

            return image_data_list

        except Exception as e:
            logger.error(f"Error generating image with GPT-Image-1: {e}")
            raise

    def get_model_info(self) -> dict[str, Any]:
        """Get GPT-Image-1 model information.

        Returns:
            Model information dictionary
        """
        return {
            "name": "GPT-Image-1",
            "model_id": self.model,
            "provider": "OpenAI",
            "capabilities": {
                "text_to_image": True,
                "image_to_image": False,
                "inpainting": False,
                "variations": False,
                "max_prompt_length": 4000,
                "supported_n": [1],
                "supports_size": False,
                "supports_style": False,
            },
            "description": "Natively multimodal LLM with image generation capabilities",
        }

    async def validate_parameters(
        self,
        prompt: str,
        size: str | None = None,
        style: str | None = None,
        n: int = 1,
        **kwargs,
    ) -> bool:
        """Validate parameters for GPT-Image-1.

        Args:
            prompt: Text description
            size: Image dimensions (ignored)
            style: Style preset (ignored)
            n: Number of images (must be 1)
            **kwargs: Additional parameters

        Returns:
            True if parameters are valid
        """
        # Check prompt length
        if not prompt or len(prompt) > 4000:
            return False

        # Check n value
        if n != 1:
            return False

        return True
