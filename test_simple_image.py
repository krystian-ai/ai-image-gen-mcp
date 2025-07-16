#!/usr/bin/env python
"""Simple test for image generation."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_image_gen_mcp.config import load_config
from ai_image_gen_mcp.models.gpt_image import GPTImageModel
from ai_image_gen_mcp.storage import LocalStorage


async def test_simple():
    """Test single image generation."""
    print("🚀 Testing GPT-Image-1...")
    
    # Load config
    config = load_config()
    print(f"✓ Config loaded, API key: {'set' if config.openai_api_key else 'missing'}")
    
    # Create model
    model = GPTImageModel(api_key=config.openai_api_key)
    print("✓ Model initialized")
    
    # Create storage
    storage = LocalStorage(config.cache_dir)
    print(f"✓ Storage initialized at: {config.cache_dir}")
    
    # Test image generation
    prompt = "A simple red circle on white background"
    print(f"\n🎨 Generating image: '{prompt}'")
    
    try:
        # Generate image
        print("⏳ Calling OpenAI API...")
        image_data_list = await model.generate(prompt=prompt, n=1)
        print(f"✓ Got {len(image_data_list)} image(s)")
        
        if image_data_list:
            # Save first image
            image_data = image_data_list[0]
            print(f"✓ Image size: {len(image_data) / 1024:.1f} KB")
            
            # Save to storage
            filename = "test_red_circle.png"
            metadata = {
                "prompt": prompt,
                "model": model.model,
                "test": "simple"
            }
            
            saved_path = await storage.save(image_data, filename, metadata)
            print(f"✓ Saved to: {saved_path}")
            
            # List files in cache dir
            print(f"\n📁 Files in cache directory:")
            cache_path = Path(config.cache_dir)
            for file in cache_path.iterdir():
                print(f"  - {file.name}")
        
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_simple())