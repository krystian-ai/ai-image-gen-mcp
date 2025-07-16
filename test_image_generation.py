#!/usr/bin/env python
"""Test script for AI Image Generation MCP Server."""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_image_gen_mcp.config import load_config
from ai_image_gen_mcp.models import ModelRouter
from ai_image_gen_mcp.storage import LocalStorage


async def test_image_generation():
    """Test image generation with real API."""
    print("🚀 Testing AI Image Generation MCP Server...\n")
    
    # Load configuration
    config = load_config()
    print(f"✓ Configuration loaded")
    print(f"  - Model: {config.model_default}")
    print(f"  - Provider: {config.model_provider}")
    print(f"  - Cache Dir: {config.cache_dir}\n")
    
    # Create storage
    storage = LocalStorage(config.cache_dir)
    print(f"✓ Storage initialized at: {config.cache_dir}\n")
    
    # Create model router
    model_router = ModelRouter.create_default_router(config)
    print(f"✓ Model router initialized")
    print(f"  - Available models: {list(model_router.models.keys())}")
    print(f"  - Default model: {model_router.default_model}\n")
    
    # Get the model
    model = model_router.get_model()
    model_info = model.get_model_info()
    print(f"✓ Using model: {model_info['name']} ({model_info['model_id']})")
    print(f"  - Provider: {model_info['provider']}")
    print(f"  - Description: {model_info['description']}\n")
    
    # Test prompts
    test_prompts = [
        "A serene mountain landscape at sunset with purple and orange sky",
        "A futuristic city with flying cars and neon lights",
        "A cute robot sitting at a desk writing code on a laptop"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"🎨 Test {i}/{len(test_prompts)}: Generating image...")
        print(f"   Prompt: \"{prompt}\"")
        
        try:
            # Validate parameters
            if not await model.validate_parameters(prompt=prompt, n=1):
                print("   ❌ Invalid parameters")
                continue
            
            # Generate image
            print("   ⏳ Calling OpenAI API...")
            image_data_list = await model.generate(prompt=prompt, n=1)
            
            if not image_data_list:
                print("   ❌ No image generated")
                continue
            
            # Save image
            filename = f"test_{i}.png"
            metadata = {
                "prompt": prompt,
                "model": model_info["model_id"],
                "test_number": i
            }
            
            image_path = await storage.save(image_data_list[0], filename, metadata)
            print(f"   ✓ Image saved to: {image_path}")
            print(f"   ✓ Size: {len(image_data_list[0]) / 1024:.1f} KB\n")
            
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {str(e)}\n")
    
    print("✅ Test completed!")
    print(f"\nGenerated images are stored in: {config.cache_dir}")


if __name__ == "__main__":
    try:
        asyncio.run(test_image_generation())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()