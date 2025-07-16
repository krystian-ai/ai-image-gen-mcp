#!/bin/bash
# Development server startup script

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies if needed
pip install -e ".[image,dev]" --quiet

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Copying from .env.example..."
    cp .env.example .env
    echo "Please edit .env and add your OpenAI API key"
    exit 1
fi

# Check if API key is set
if grep -q "sk-your-openai-api-key-here" .env; then
    echo "⚠️  Please update OPENAI_API_KEY in .env file"
    exit 1
fi

echo "🚀 Starting AI Image Generation MCP Server..."
python -m ai_image_gen_mcp.server stdio