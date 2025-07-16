# Examples

This directory contains example scripts demonstrating how to use the AI Image Generation MCP Server.

## Basic Usage

### `basic_usage.py`
Simple example showing how to generate an image with the default model (DALL-E 3).

```bash
export OPENAI_API_KEY='your-api-key'
python examples/basic_usage.py
```

### `multiple_models.py`
Demonstrates using different AI models (DALL-E 3, DALL-E 2, GPT-Image-1).

```bash
export OPENAI_API_KEY='your-api-key'
python examples/multiple_models.py
```

## Configuration Examples

### `claude_desktop_config.example.json`
Example configuration for Claude Desktop integration. Copy this to your Claude Desktop config location and update the paths:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

## Testing Scripts

The `testing/` subdirectory contains various test scripts used during development. These are kept for reference but are not part of the main examples.

## Tips

1. Always set your OpenAI API key before running examples
2. Images are saved to `/tmp/ai-image-gen-cache` by default
3. You can customize the cache directory with the `CACHE_DIR` environment variable
4. Check the generated `.json` metadata files for prompt and model information