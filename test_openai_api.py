#!/usr/bin/env python
"""Test OpenAI API connection."""

import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

async def test_openai():
    """Test OpenAI API connection."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No OpenAI API key found in environment")
        return
    
    print(f"✓ API Key found: {api_key[:8]}...{api_key[-4:]}")
    
    # Test with regular chat completion first
    client = AsyncOpenAI(api_key=api_key)
    
    try:
        print("\n🧪 Testing basic OpenAI connection with chat completion...")
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=10
        )
        print(f"✓ Basic API works: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ Basic API failed: {type(e).__name__}: {str(e)}")
        return
    
    # Check if responses API exists
    print("\n🧪 Checking for responses API...")
    try:
        if hasattr(client, 'responses'):
            print("✓ Client has responses attribute")
            # Try to call it
            response = await client.responses.create(
                model="gpt-4.1-mini",
                input="Test",
                tools=[{"type": "image_generation"}]
            )
            print("✓ Responses API call succeeded!")
            print(f"  Response type: {type(response)}")
            print(f"  Status: {response.status}")
            print(f"  Output: {response.output}")
            if hasattr(response, 'output_text'):
                print(f"  Output text: {response.output_text}")
            if hasattr(response, 'text'):
                print(f"  Text: {response.text}")
        else:
            print("❌ Client does not have 'responses' attribute")
            print("  Available attributes:", [attr for attr in dir(client) if not attr.startswith('_')])
    except Exception as e:
        print(f"❌ Responses API failed: {type(e).__name__}: {str(e)}")
    
    # Try DALL-E 3 instead
    print("\n🧪 Testing DALL-E 3 image generation...")
    try:
        response = await client.images.generate(
            model="dall-e-3",
            prompt="A simple red circle on white background",
            size="1024x1024",
            quality="standard",
            n=1
        )
        print(f"✓ DALL-E 3 works! Image URL: {response.data[0].url[:50]}...")
    except Exception as e:
        print(f"❌ DALL-E 3 failed: {type(e).__name__}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_openai())