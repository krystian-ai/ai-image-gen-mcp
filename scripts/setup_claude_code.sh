#!/bin/bash
# Setup script for Claude Code CLI integration

echo "🚀 Setting up AI Image Generation MCP for Claude Code CLI"

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if .env exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "❌ .env file not found. Please create it from .env.example"
    exit 1
fi

# Load .env to get API key
source "$PROJECT_DIR/.env"

if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY not set in .env file"
    exit 1
fi

# Create MCP config for current directory
mkdir -p .claude
cat > .claude/mcp.json << EOF
{
  "servers": [
    {
      "name": "ai-image-gen",
      "command": "$PROJECT_DIR/.venv/bin/python",
      "args": ["-m", "ai_image_gen_mcp.server", "stdio"],
      "env": {
        "PYTHONPATH": "$PROJECT_DIR/src",
        "OPENAI_API_KEY": "$OPENAI_API_KEY"
      }
    }
  ]
}
EOF

echo "✅ Created .claude/mcp.json in current directory"
echo ""
echo "📝 Usage:"
echo "   1. Run 'claude code' in this directory"
echo "   2. Ask Claude to generate images:"
echo "      'Generate a hero background image - modern tech theme'"
echo ""
echo "🖼️  Images will be saved to: /tmp/ai-image-gen-cache/"
echo ""
echo "💡 Tip: Copy generated images to your project:"
echo "   cp /tmp/ai-image-gen-cache/[filename].png ./assets/images/"