#!/usr/bin/env python
"""Test server startup with a simple JSON-RPC request."""

import asyncio
import json
import subprocess
import sys
from pathlib import Path

async def test_server():
    """Test server with a simple request."""
    # Start the server process
    cmd = [sys.executable, "-m", "ai_image_gen_mcp.server", "stdio"]
    env = {
        **subprocess.os.environ,
        "PYTHONPATH": str(Path(__file__).parent / "src")
    }
    
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    
    print("✓ Server process started")
    
    # Send initialize request
    init_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "0.1.0",
            "capabilities": {}
        }
    }
    
    request_str = json.dumps(init_request) + "\n"
    proc.stdin.write(request_str.encode())
    await proc.stdin.drain()
    print("✓ Sent initialize request")
    
    # Read response
    try:
        response_line = await asyncio.wait_for(proc.stdout.readline(), timeout=5.0)
        response = json.loads(response_line.decode())
        print(f"✓ Got response: {response.get('result', {}).get('protocolVersion', 'unknown')}")
    except asyncio.TimeoutError:
        print("❌ No response received within 5 seconds")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Check stderr for any errors
    stderr_task = asyncio.create_task(proc.stderr.read())
    await asyncio.sleep(0.5)
    
    if stderr_task.done():
        stderr_output = stderr_task.result().decode()
        if stderr_output:
            print("\n📋 Server logs:")
            for line in stderr_output.split('\n'):
                if line.strip():
                    print(f"  {line}")
    
    # Terminate server
    proc.terminate()
    await proc.wait()
    print("\n✓ Server terminated")

if __name__ == "__main__":
    asyncio.run(test_server())