# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server for AI image generation. The project is currently in its initial planning phase with comprehensive documentation but no implementation yet.

## Development Commands

### Setup
```bash
# Create virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -e .[image,dev]

# Copy environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running the Server
```bash
# Via MCP CLI
mcp-imageserve stdio

# Direct Python execution
python -m ai_image_gen_mcp.server --transport=stdio
```

### Code Quality
The project will use pre-commit hooks with:
- black (code formatting)
- ruff (linting)
- mypy (type checking)

## Architecture

The MCP server follows a modular architecture:

1. **MCP Server Layer**: Handles JSON-RPC 2.0 protocol, validates requests, manages authentication
2. **Model Router**: Strategy pattern for switching between AI models (GPT-Image-1, DALL·E, Stable Diffusion)
3. **Object Storage**: Stores generated images and provides signed URLs
4. **Async Queue**: Celery/Kafka for GPU task management
5. **Post-Processing Pipeline**: Image enhancement and watermarking

### Key MCP Primitives
- **Tools**: `generate_image`, `upscale_image`, `inpaint_image`
- **Resources**: Generated assets, prompt logs, experiment metadata
- **Prompts**: Reusable templates for image generation

## Important Notes

- **Python Version**: 3.11+ required
- **MVP Model**: GPT-Image-1 (OpenAI) - requires OPENAI_API_KEY
- **Configuration**: Uses `.env` file for API keys and settings
- **Target MVP Date**: September 30, 2025

## Current Status

The project now has a complete MVP implementation:
1. **MCP Server**: Implemented with FastMCP, exposes `generate_image` tool and model resources
2. **Multiple Models**: 
   - DALL-E 3 (default) - High quality, supports sizes and styles
   - DALL-E 2 - Previous generation, supports multiple images
   - GPT-Image-1 - Uses Responses API (slower, timeout issues)
3. **Local Storage**: Saves generated images with metadata to configurable cache directory
4. **Configuration**: Environment-based configuration via .env file
5. **Testing**: Comprehensive test suite with 100% test pass rate

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_image_gen_mcp

# Run specific test file
pytest tests/test_server.py

# Test actual image generation
python test_dalle.py
python test_image_generation.py
```

### Linting and Type Checking
```bash
# Format code
black src/

# Lint
ruff check src/

# Type check
mypy src/
```

## Key Implementation Details

### Models
1. **DALL-E 3** (Default):
   - Uses OpenAI Images API (`/v1/images/generations`)
   - Supports sizes: 1024x1024, 1792x1024, 1024x1792
   - Supports styles: vivid, natural
   - Limited to n=1
   - High quality output

2. **DALL-E 2**:
   - Uses OpenAI Images API
   - Supports sizes: 256x256, 512x512, 1024x1024
   - Supports n=1-10
   - Good for batch generation

3. **GPT-Image-1**:
   - Uses Responses API (`/v1/responses`)
   - Model: `gpt-4.1-mini` with `tools=[{"type": "image_generation"}]`
   - Base64-encoded images in response
   - No size/style parameters, only n=1
   - Slower, may timeout (20+ seconds)

### Storage
- Local filesystem with timestamp-based unique filenames
- Metadata saved as JSON alongside images
- Future migration path to S3/GCS

## Known Issues

1. GPT-Image-1 responses can take 20+ seconds, may timeout
2. Claude Desktop integration requires full venv path
3. OPENAI_API_KEY must be set in environment or .env file