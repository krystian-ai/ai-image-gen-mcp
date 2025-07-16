#!/usr/bin/env python
"""Example showing how to use different AI models."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_image_gen_mcp.config import load_config
from ai_image_gen_mcp.models import ModelRouter
from ai_image_gen_mcp.storage import LocalStorage


async def generate_with_model(model_router, storage, model_name, prompt, **kwargs):
    """Generate an image with a specific model."""
    print(f"\n🎨 Using {model_name}...")
    
    try:
        # Get specific model
        model = model_router.get_model(model_name)
        model_info = model.get_model_info()
        
        print(f"   Model: {model_info['name']} ({model_info['model_id']})")
        print(f"   Provider: {model_info['provider']}")
        
        # Generate image
        image_data_list = await model.generate(prompt=prompt, **kwargs)
        
        if image_data_list:
            # Save the first image
            image_data = image_data_list[0]
            filename = f"{model_name}_example.png"
            metadata = {
                "prompt": prompt,
                "model": model_name,
                "example": "multiple_models",
                **kwargs
            }
            
            saved_path = await storage.save(image_data, filename, metadata)
            print(f"   ✓ Saved to: {saved_path}")
            print(f"   ✓ Size: {len(image_data) / 1024:.1f} KB")
            
    except Exception as e:
        print(f"   ❌ Error: {type(e).__name__}: {str(e)}")


async def main():
    """Demonstrate using different models."""
    print("🤖 Multiple Models Example\n")
    
    # Load configuration
    config = load_config()
    storage = LocalStorage(config.cache_dir)
    model_router = ModelRouter.create_default_router(config)
    
    print(f"Available models: {list(model_router.models.keys())}")
    
    # Common prompt
    prompt = "A cute robot assistant helping a programmer write code, cartoon style"
    
    # Test DALL-E 3 (default)
    await generate_with_model(
        model_router, storage, "dalle-3", prompt,
        size="1024x1024",
        style="vivid"
    )
    
    # Test DALL-E 2
    await generate_with_model(
        model_router, storage, "dalle-2", prompt,
        size="512x512",
        n=1
    )
    
    # Test GPT-Image-1 (if you want to wait)
    print("\n⚠️  GPT-Image-1 can take 20+ seconds...")
    response = input("Test GPT-Image-1? (y/N): ")
    if response.lower() == 'y':
        await generate_with_model(
            model_router, storage, "gpt-image-1", prompt,
            n=1  # Only supports n=1
        )
    
    print(f"\n✓ All images saved to: {config.cache_dir}")


if __name__ == "__main__":
    # Check for API key
    import os
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Please set OPENAI_API_KEY environment variable")
        sys.exit(1)
    
    asyncio.run(main())