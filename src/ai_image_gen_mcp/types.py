"""Type definitions for the AI Image Generation MCP Server."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


class ImageGenerationRequest(BaseModel):
    """Schema for image generation requests."""
    
    prompt: str = Field(
        ...,
        description="Text description of the desired image",
        min_length=1,
        max_length=4000
    )
    style: Optional[Literal["default", "photorealistic", "illustration"]] = Field(
        default="default",
        description="Style preset for image generation"
    )
    size: Optional[Literal["1024x1024", "1792x1024", "1024x1792"]] = Field(
        default="1024x1024",
        description="Image dimensions"
    )
    n: Optional[int] = Field(
        default=1,
        description="Number of images to generate",
        ge=1,
        le=1  # GPT-Image-1 only supports n=1
    )


class ImageGenerationResponse(BaseModel):
    """Response schema for image generation."""
    
    image_urls: list[str] = Field(
        ...,
        description="URLs or paths to generated images"
    )
    prompt: str = Field(
        ...,
        description="The prompt used for generation"
    )
    model: str = Field(
        ...,
        description="Model used for generation"
    )
    created_at: str = Field(
        ...,
        description="ISO 8601 timestamp of generation"
    )