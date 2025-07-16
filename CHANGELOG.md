# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-16

### Added
- Initial release of AI Image Generation MCP Server
- Support for multiple AI models:
  - DALL-E 3 (default) - High quality image generation
  - DALL-E 2 - Previous generation with batch support
  - GPT-Image-1 - Experimental multimodal model
- MCP server implementation with FastMCP
- Local filesystem storage with metadata tracking
- Comprehensive test suite
- Example scripts for basic and advanced usage
- Claude Desktop integration support
- Environment-based configuration
- Built-in prompt templates for common use cases

### Technical Details
- Python 3.11+ support
- Async/await architecture
- Type hints throughout
- Extensible model router system
- JSON-RPC 2.0 protocol compliance

### Known Issues
- GPT-Image-1 responses can take 20+ seconds
- Only local storage is currently supported (S3/GCS planned)

[0.1.0]: https://github.com/krystian-ai/ai-image-gen-mcp/releases/tag/v0.1.0