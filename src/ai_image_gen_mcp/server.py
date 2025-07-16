"""Main MCP server implementation for AI Image Generation."""

import sys
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from .config import load_config
from .types import ImageGenerationRequest, ImageGenerationResponse
from .models import ModelRouter
from .storage import LocalStorage


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Important: MCP servers must not write to stdout
)
logger = logging.getLogger(__name__)


# Initialize server
mcp = FastMCP("AI Image Generation MCP Server")

# Global instances (will be initialized in main)
config = None
model_router = None
storage = None


@mcp.tool()
async def generate_image(
    prompt: str,
    style: Optional[str] = "default",
    size: Optional[str] = "1024x1024",
    n: Optional[int] = 1
) -> ImageGenerationResponse:
    """Generate images from text descriptions using AI models.
    
    Args:
        prompt: Text description of the desired image
        style: Style preset (default, photorealistic, illustration)
        size: Image dimensions (1024x1024, 1792x1024, 1024x1792)
        n: Number of images to generate (currently only 1 supported)
        
    Returns:
        ImageGenerationResponse with image URLs and metadata
    """
    logger.info(f"Generating image with prompt: {prompt[:50]}...")
    
    # Validate request
    request = ImageGenerationRequest(
        prompt=prompt,
        style=style,
        size=size,
        n=n
    )
    
    # Get model (use default for now)
    model = model_router.get_model()
    
    # Validate parameters for the model
    if not await model.validate_parameters(
        prompt=request.prompt,
        size=request.size,
        style=request.style,
        n=request.n
    ):
        raise ValueError("Invalid parameters for selected model")
    
    # Generate images
    try:
        image_data_list = await model.generate(
            prompt=request.prompt,
            size=request.size,
            style=request.style,
            n=request.n
        )
    except Exception as e:
        logger.error(f"Model generation failed: {e}")
        raise RuntimeError(f"Image generation failed: {str(e)}")
    
    # Save images to storage
    image_urls = []
    for idx, image_data in enumerate(image_data_list):
        filename = f"generated_{idx}.png"
        metadata = {
            "prompt": request.prompt,
            "style": request.style,
            "size": request.size,
            "model": model.get_model_info()["model_id"],
            "created_at": datetime.utcnow().isoformat()
        }
        
        try:
            url = await storage.save(image_data, filename, metadata)
            image_urls.append(url)
        except Exception as e:
            logger.error(f"Storage save failed: {e}")
            raise RuntimeError(f"Failed to save image: {str(e)}")
    
    # Return response
    response = ImageGenerationResponse(
        image_urls=image_urls,
        prompt=request.prompt,
        model=model.get_model_info()["model_id"],
        created_at=datetime.utcnow().isoformat()
    )
    
    logger.info(f"Successfully generated {len(image_urls)} image(s)")
    return response


@mcp.resource("models://list")
async def list_models() -> dict:
    """List available image generation models.
    
    Returns:
        Dictionary containing available models and their capabilities
    """
    return {
        "models": model_router.list_models(),
        "default": model_router.default_model
    }


@mcp.prompt()
async def product_mockup(
    product_name: str,
    style: str = "photorealistic",
    background: str = "white studio"
) -> str:
    """Generate a product mockup prompt.
    
    Args:
        product_name: Name of the product
        style: Visual style
        background: Background description
        
    Returns:
        Formatted prompt for product mockup generation
    """
    return f"High-quality {style} product photography of {product_name}, professional lighting, {background} background, commercial photography, detailed textures, 8k resolution"


@mcp.prompt()
async def concept_art(
    subject: str,
    art_style: str = "digital painting",
    mood: str = "dramatic"
) -> str:
    """Generate a concept art prompt.
    
    Args:
        subject: Main subject of the artwork
        art_style: Artistic style
        mood: Mood or atmosphere
        
    Returns:
        Formatted prompt for concept art generation
    """
    return f"{mood} {art_style} concept art of {subject}, professional artwork, detailed composition, atmospheric lighting, trending on artstation"


def main():
    """Main entry point for the MCP server."""
    global config, model_router, storage
    
    # Load configuration
    config = load_config()
    
    # Set logging level from config
    logging.getLogger().setLevel(config.log_level)
    
    # Initialize components
    logger.info("Initializing AI Image Generation MCP Server...")
    
    # Create storage backend
    storage = LocalStorage(config.cache_dir)
    logger.info(f"Storage initialized at: {config.cache_dir}")
    
    # Create model router
    model_router = ModelRouter.create_default_router(config)
    logger.info(f"Model router initialized with models: {list(model_router.models.keys())}")
    
    # Run the server
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    
    if transport == "stdio":
        logger.info("Starting server with stdio transport...")
        import asyncio
        asyncio.run(mcp.run())
    else:
        logger.error(f"Unknown transport: {transport}")
        sys.exit(1)


if __name__ == "__main__":
    main()