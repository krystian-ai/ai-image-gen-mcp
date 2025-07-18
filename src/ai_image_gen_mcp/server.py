"""Main MCP server implementation for AI Image Generation."""

import logging
import sys
from datetime import datetime

from mcp.server.fastmcp import FastMCP

from .config import load_config
from .models import ModelRouter
from .storage import LocalStorage
from .types import ImageGenerationRequest, ImageGenerationResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,  # Important: MCP servers must not write to stdout
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
    style: str | None = "default",
    size: str | None = "1024x1024",
    n: int | None = 1,
    model: str | None = None,
) -> ImageGenerationResponse:
    """Generate images from text descriptions using AI models.

    Args:
        prompt: Text description of the desired image
        style: Style preset (default, photorealistic, illustration)
        size: Image dimensions (1024x1024, 1792x1024, 1024x1792)
        n: Number of images to generate (currently only 1 supported)
        model: Specific model to use (dalle-3, dalle-2, gpt-image-1)

    Returns:
        ImageGenerationResponse with image URLs and metadata
    """
    logger.info(f"Generating image with prompt: {prompt[:50]}...")

    # Validate request
    request = ImageGenerationRequest(prompt=prompt, style=style, size=size, n=n)

    # Ensure model_router is initialized
    if model_router is None:
        raise RuntimeError("Server not initialized. Please restart the MCP server.")

    # Get model (use specified model or default)
    try:
        selected_model = model_router.get_model(model)
        if model:
            logger.info(f"Using specified model: {model}")
    except ValueError as e:
        logger.warning(f"Model '{model}' not found, using default")
        selected_model = model_router.get_model()

    model = selected_model

    # Validate parameters for the model
    if not await model.validate_parameters(
        prompt=request.prompt, size=request.size, style=request.style, n=request.n
    ):
        raise ValueError("Invalid parameters for selected model")

    # Generate images
    try:
        image_data_list = await model.generate(
            prompt=request.prompt, size=request.size, style=request.style, n=request.n
        )
    except Exception as e:
        logger.error(f"Model generation failed: {e}")
        raise RuntimeError(f"Image generation failed: {str(e)}") from e

    # Save images to storage
    image_urls = []
    for idx, image_data in enumerate(image_data_list):
        filename = f"generated_{idx}.png"
        metadata = {
            "prompt": request.prompt,
            "style": request.style,
            "size": request.size,
            "model": model.get_model_info()["model_id"],
            "created_at": datetime.utcnow().isoformat(),
        }

        try:
            url = await storage.save(image_data, filename, metadata)
            image_urls.append(url)
        except Exception as e:
            logger.error(f"Storage save failed: {e}")
            raise RuntimeError(f"Failed to save image: {str(e)}") from e

    # Create user-friendly message
    if image_urls:
        message = f"✅ Image generated successfully!\n\n📁 Location: {image_urls[0]}\n\nYou can open this file directly to view the image."
    else:
        message = "❌ No images were generated"

    # Return response
    response = ImageGenerationResponse(
        image_urls=image_urls,
        prompt=request.prompt,
        model=model.get_model_info()["model_id"],
        created_at=datetime.utcnow().isoformat(),
        message=message,
    )

    logger.info(f"Successfully generated {len(image_urls)} image(s)")

    # Add a helpful message about the image location
    if image_urls:
        logger.info(f"Image saved at: {image_urls[0]}")

    return response


@mcp.resource("images://{path}")
async def get_image(path: str) -> dict:
    """Serve an image file as a resource.

    Args:
        path: Path to the image file

    Returns:
        Image data as base64 with metadata
    """
    import base64
    from pathlib import Path

    try:
        image_path = Path(path.replace("images://", ""))

        if not image_path.exists():
            return {"error": f"Image not found: {image_path}"}

        # Read image data
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Convert to base64
        base64_data = base64.b64encode(image_data).decode("utf-8")

        # Determine MIME type
        suffix = image_path.suffix.lower()
        mime_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
        }
        mime_type = mime_types.get(suffix, "image/png")

        return {
            "type": "image",
            "data": f"data:{mime_type};base64,{base64_data}",
            "path": str(image_path),
            "size": len(image_data),
            "mime_type": mime_type,
        }
    except Exception as e:
        logger.error(f"Failed to serve image: {e}")
        return {"error": str(e)}


@mcp.resource("models://list")
async def list_models() -> dict:
    """List available image generation models.

    Returns:
        Dictionary containing available models and their capabilities
    """
    return {"models": model_router.list_models(), "default": model_router.default_model}


@mcp.prompt()
async def product_mockup(
    product_name: str, style: str = "photorealistic", background: str = "white studio"
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
    subject: str, art_style: str = "digital painting", mood: str = "dramatic"
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


def main() -> None:
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
    logger.info(
        f"Model router initialized with models: {list(model_router.models.keys())}"
    )

    # Run the server
    transport = sys.argv[1] if len(sys.argv) > 1 else "stdio"

    if transport == "stdio":
        logger.info("Starting server with stdio transport...")
        mcp.run(transport="stdio")
    else:
        logger.error(f"Unknown transport: {transport}")
        sys.exit(1)


if __name__ == "__main__":
    main()
