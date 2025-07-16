"""Tests for model implementations."""

import pytest
import base64
from unittest.mock import AsyncMock, patch
from ai_image_gen_mcp.models.gpt_image import GPTImageModel


@pytest.mark.asyncio
async def test_gpt_image_generate_success():
    """Test successful GPT-Image-1 generation."""
    # Create model instance
    model = GPTImageModel(api_key="sk-test")
    
    # Mock OpenAI client
    mock_response = AsyncMock()
    mock_output = AsyncMock()
    mock_output.type = "image_generation_call"
    mock_output.result = base64.b64encode(b"test_image_data").decode()
    mock_response.output = [mock_output]
    
    with patch.object(model.client.responses, 'create', return_value=mock_response):
        # Generate image
        images = await model.generate("A test image", n=1)
        
        # Assertions
        assert len(images) == 1
        assert images[0] == b"test_image_data"


@pytest.mark.asyncio
async def test_gpt_image_validate_parameters():
    """Test parameter validation for GPT-Image-1."""
    model = GPTImageModel(api_key="sk-test")
    
    # Valid parameters
    assert await model.validate_parameters("Valid prompt", n=1) is True
    
    # Invalid n value
    assert await model.validate_parameters("Valid prompt", n=2) is False
    
    # Too long prompt
    assert await model.validate_parameters("x" * 4001, n=1) is False
    
    # Empty prompt
    assert await model.validate_parameters("", n=1) is False


def test_gpt_image_model_info():
    """Test model info retrieval."""
    model = GPTImageModel(api_key="sk-test", model="gpt-4.1-mini")
    info = model.get_model_info()
    
    assert info["name"] == "GPT-Image-1"
    assert info["model_id"] == "gpt-4.1-mini"
    assert info["provider"] == "OpenAI"
    assert info["capabilities"]["text_to_image"] is True
    assert info["capabilities"]["supported_n"] == [1]