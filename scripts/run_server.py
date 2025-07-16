#!/usr/bin/env python
"""Development script to run the MCP server."""

import sys
import os
from pathlib import Path

# Add parent directory to path for development
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_image_gen_mcp.server import main

if __name__ == "__main__":
    main()