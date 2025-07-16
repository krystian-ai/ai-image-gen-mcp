"""Tests for the MCP server implementation."""

import pytest
from unittest.mock import Mock, AsyncMock, patch
from ai_image_gen_mcp.server import generate_image
from ai_image_gen_mcp.types import ImageGenerationResponse


@pytest.mark.asyncio
async def test_generate_image_success():
    """Test successful image generation."""
    # Mock dependencies
    with (
        patch("ai_image_gen_mcp.server.model_router") as mock_router,
        patch("ai_image_gen_mcp.server.storage") as mock_storage,
    ):

        # Setup mocks
        mock_model = AsyncMock()
        mock_model.validate_parameters.return_value = True
        mock_model.generate.return_value = [b"fake_image_data"]
        mock_model.get_model_info = Mock(return_value={"model_id": "gpt-4.1-mini"})

        mock_router.get_model.return_value = mock_model
        mock_storage.save = AsyncMock(return_value="/tmp/generated_0.png")

        # Call function
        response = await generate_image(
            prompt="A beautiful sunset", style="photorealistic", size="1024x1024", n=1
        )

        # Assertions
        assert isinstance(response, ImageGenerationResponse)
        assert len(response.image_urls) == 1
        assert response.image_urls[0] == "/tmp/generated_0.png"
        assert response.prompt == "A beautiful sunset"
        assert response.model == "gpt-4.1-mini"


@pytest.mark.asyncio
async def test_generate_image_invalid_parameters():
    """Test image generation with invalid parameters."""
    # Test Pydantic validation error for n > 1
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        await generate_image(prompt="Test", n=5)  # Invalid for GPT-Image-1
