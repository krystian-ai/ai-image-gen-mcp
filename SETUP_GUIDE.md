# AI Image Generation MCP Server - Setup Guide

## Prerequisites

- Python 3.11 or higher
- OpenAI API key
- Claude Desktop (for testing)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/krystian-ai/ai-image-gen-mcp.git
cd ai-image-gen-mcp
```

### 2. Set Up Virtual Environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -e ".[image,dev]"
```

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 5. Test the Server

Run tests to ensure everything is working:
```bash
pytest
```

Test server startup:
```bash
python -m ai_image_gen_mcp.server stdio
```
(Press Ctrl+C to stop)

## Claude Desktop Integration

### Option 1: Using pip-installed package

After installation, add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "ai-image-gen": {
      "command": "mcp-imageserve",
      "args": ["stdio"],
      "transport": "STDIO"
    }
  }
}
```

### Option 2: Development mode

For development, use the full path to your virtual environment:
```json
{
  "mcpServers": {
    "ai-image-gen": {
      "command": "/path/to/ai-image-gen-mcp/.venv/bin/python",
      "args": [
        "-m",
        "ai_image_gen_mcp.server",
        "stdio"
      ],
      "transport": "STDIO",
      "env": {
        "PYTHONPATH": "/path/to/ai-image-gen-mcp/src",
        "OPENAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Note: Replace `/path/to/ai-image-gen-mcp` with your actual project path and add your OpenAI API key.

### Claude Desktop Config Location

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

## Usage in Claude Desktop

After restarting Claude Desktop, you should see the image generation tools available:

1. **Generate Image**: Use the `/image` tool
   ```
   /image "A beautiful sunset over mountains"
   ```

2. **Product Mockup**: Use the prompt template
   ```
   Use the product_mockup prompt for "wireless headphones"
   ```

3. **List Models**: Check available models
   ```
   Show me the available image generation models
   ```

## Troubleshooting

### Server won't start
- Check Python version: `python --version` (must be 3.11+)
- Verify OpenAI API key is set in `.env`
- Check logs in stderr output

### Claude Desktop doesn't show the server
- Ensure Claude Desktop is fully closed before editing config
- Check JSON syntax in config file
- Verify paths are absolute, not relative
- Check Claude Desktop logs for errors

### Image generation fails
- Verify OpenAI API key is valid
- Check API quota/limits on OpenAI dashboard
- Review server logs for specific error messages

## Development

### Running Tests
```bash
pytest -v
```

### Linting
```bash
ruff check src/
black src/
mypy src/
```

### Adding New Models
See `src/ai_image_gen_mcp/models/` for examples of implementing new models.