#!/usr/bin/env python
"""Basic example of using the AI Image Generation MCP Server."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_image_gen_mcp.config import load_config
from ai_image_gen_mcp.models import ModelRouter
from ai_image_gen_mcp.storage import LocalStorage


async def main():
    """Generate a simple image using the default model."""
    print("🎨 AI Image Generation Example\n")
    
    # Load configuration
    config = load_config()
    
    # Create storage
    storage = LocalStorage(config.cache_dir)
    print(f"✓ Storage initialized at: {config.cache_dir}")
    
    # Create model router
    model_router = ModelRouter.create_default_router(config)
    print(f"✓ Available models: {list(model_router.models.keys())}")
    print(f"✓ Using default model: {model_router.default_model}\n")
    
    # Get the default model
    model = model_router.get_model()
    
    # Generate an image
    prompt = "A beautiful sunset over a calm ocean with vibrant orange and purple colors"
    print(f"🖼️  Generating: '{prompt}'")
    
    try:
        # Generate image
        image_data_list = await model.generate(
            prompt=prompt,
            size="1792x1024",  # Wide format
            style="vivid",     # Vivid style for DALL-E 3
            n=1
        )
        
        # Save the image
        if image_data_list:
            image_data = image_data_list[0]
            filename = "sunset_ocean.png"
            metadata = {
                "prompt": prompt,
                "model": model.get_model_info()["model_id"],
                "example": "basic_usage"
            }
            
            saved_path = await storage.save(image_data, filename, metadata)
            print(f"✓ Image saved to: {saved_path}")
            print(f"✓ Size: {len(image_data) / 1024:.1f} KB")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    # Check for API key
    import os
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set OPENAI_API_KEY environment variable")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    asyncio.run(main())