#!/bin/bash
# Test Claude Code MCP integration

echo "🧪 Testing Claude Code MCP Integration"
echo ""

# Check if config exists
CONFIG_LOCATIONS=(
    "$HOME/.config/claude/mcp_settings.json"
    "$HOME/.claude/mcp_settings.json"
)

FOUND=false
for config in "${CONFIG_LOCATIONS[@]}"; do
    if [ -f "$config" ]; then
        echo "✅ Found MCP config at: $config"
        echo "📄 Content:"
        cat "$config" | jq '.' 2>/dev/null || cat "$config"
        FOUND=true
        break
    fi
done

if [ "$FOUND" = false ]; then
    echo "❌ No MCP configuration found"
    echo "   Expected locations:"
    for config in "${CONFIG_LOCATIONS[@]}"; do
        echo "   - $config"
    done
    exit 1
fi

echo ""
echo "🔍 Checking server setup..."

# Check if server script exists
SERVER_PATH="/Users/kkaczynski/Sources/projects-ai/ai-image-gen-mcp/.venv/bin/python"
if [ -f "$SERVER_PATH" ]; then
    echo "✅ Python venv found"
else
    echo "❌ Python venv not found at: $SERVER_PATH"
    exit 1
fi

# Check if module is importable
cd /Users/kkaczynski/Sources/projects-ai/ai-image-gen-mcp
source .venv/bin/activate
if python -c "import ai_image_gen_mcp.server" 2>/dev/null; then
    echo "✅ MCP server module is importable"
else
    echo "❌ Cannot import MCP server module"
    exit 1
fi

# Check environment
if [ -n "$OPENAI_API_KEY" ]; then
    echo "✅ OPENAI_API_KEY is set"
else
    echo "❌ OPENAI_API_KEY not found in environment"
fi

echo ""
echo "📝 Next steps:"
echo "   1. Start a new terminal (to load environment)"
echo "   2. Run: claude"
echo "   3. Ask: 'Generate an image of a sunset'"
echo ""
echo "💡 The MCP server should activate automatically when Claude Code needs it"