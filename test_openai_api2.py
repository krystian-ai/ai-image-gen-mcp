#!/usr/bin/env python
"""Test different approaches to OpenAI image generation."""

import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

async def test_approaches():
    """Test different approaches to image generation."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        return
    
    print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")
    client = AsyncOpenAI(api_key=api_key)
    
    # Test 1: Try responses API with image generation prompt
    print("\n🧪 Test 1: Responses API with image generation prompt...")
    try:
        response = await client.responses.create(
            model="gpt-4.1-mini",
            input="Generate an image of a red circle on white background",
            tools=[{"type": "image_generation"}],
            tool_choice={"type": "image_generation"}
        )
        print(f"✓ Response status: {response.status}")
        
        # Extract image data
        if response.output and len(response.output) > 0:
            first_output = response.output[0]
            if hasattr(first_output, 'result'):
                print(f"  Got base64 image data! Length: {len(first_output.result)}")
                # Save a small preview
                import base64
                image_data = base64.b64decode(first_output.result)
                print(f"  Decoded image size: {len(image_data)} bytes")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {str(e)}")
    
    # Test 2: DALL-E 3 API (we know this works)
    print("\n🧪 Test 2: DALL-E 3 direct API...")
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt="A simple red circle on white background",
            size="1024x1024",
            quality="standard",
            n=1
        )
        print(f"✓ Image URL: {response.data[0].url[:50]}...")
        
        # Check what else is in the response
        print(f"  Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
        print(f"  Data attributes: {[attr for attr in dir(response.data[0]) if not attr.startswith('_')]}")
        
        # Check if we can get the image data
        if hasattr(response.data[0], 'b64_json'):
            print(f"  Has b64_json: {response.data[0].b64_json is not None}")
        
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {str(e)}")
    
    # Test 3: DALL-E 3 with response_format
    print("\n🧪 Test 3: DALL-E 3 with base64 response format...")
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt="A simple blue square on white background",
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="b64_json"
        )
        print("✓ Got base64 response")
        print(f"  Base64 data length: {len(response.data[0].b64_json) if response.data[0].b64_json else 0}")
        print(f"  Revised prompt: {response.data[0].revised_prompt}")
        
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {str(e)}")
    
    # Test 4: Check available models
    print("\n🧪 Test 4: Check available models...")
    try:
        models = await client.models.list()
        image_models = [m for m in models.data if 'dall' in m.id.lower() or 'image' in m.id.lower()]
        print(f"✓ Found {len(image_models)} image-related models:")
        for model in image_models:
            print(f"  - {model.id}")
    except Exception as e:
        print(f"❌ Failed: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_approaches())