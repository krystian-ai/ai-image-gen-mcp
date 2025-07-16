#!/usr/bin/env python
"""Debug test for OpenAI responses API."""

import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv


async def test_debug():
    """Debug the responses API call."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"✓ API key: {api_key[:8]}...{api_key[-4:]}")
    
    # Create client
    print("Creating client...")
    client = AsyncOpenAI(api_key=api_key)
    print("✓ Client created")
    
    # Try a simple call
    print("\n🧪 Testing responses.create...")
    try:
        print("Making API call...")
        response = await asyncio.wait_for(
            client.responses.create(
                model="gpt-4.1-mini",
                input="Generate a simple red circle",
                tools=[{"type": "image_generation"}],
                tool_choice={"type": "image_generation"}
            ),
            timeout=20.0
        )
        print(f"✓ Got response: {response.status}")
        
    except asyncio.TimeoutError:
        print("❌ API call timed out after 20 seconds")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_debug())