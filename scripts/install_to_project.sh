#!/bin/bash
# Install AI Image Generation MCP to any project for Claude Code

echo "🚀 Installing AI Image Generation MCP for Claude Code"

# Get the directory where script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MCP_PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Check if we're in a project directory
if [ "$PWD" == "$MCP_PROJECT_DIR" ]; then
    echo "❌ Don't run this in the MCP project directory itself!"
    echo "   Change to your web project directory first."
    exit 1
fi

# Create .mcp.json in current directory
cat > .mcp.json << EOF
{
  "mcpServers": {
    "ai-image-gen": {
      "command": "${MCP_PROJECT_DIR}/.venv/bin/python",
      "args": [
        "-m",
        "ai_image_gen_mcp.server",
        "stdio"
      ],
      "env": {
        "PYTHONPATH": "${MCP_PROJECT_DIR}/src",
        "OPENAI_API_KEY": "\${OPENAI_API_KEY}"
      }
    }
  }
}
EOF

echo "✅ Created .mcp.json in $(pwd)"
echo ""
echo "📝 Usage:"
echo "   1. Open Claude Code in this directory: 'claude code .'"
echo "   2. Claude will prompt to approve the MCP server"
echo "   3. Once approved, you can generate images:"
echo "      'Generate a hero background image'"
echo ""
echo "🖼️  Images will be saved to: /tmp/ai-image-gen-cache/"
echo ""
echo "💡 Example prompts:"
echo "   - 'Create a landing page hero background'"
echo "   - 'Generate product placeholder images'"
echo "   - 'Make a banner 1792x1024 with tech theme'"