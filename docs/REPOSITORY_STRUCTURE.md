# Repository Structure

This document describes the organization of the AI Image Generation MCP Server repository.

```
ai-image-gen-mcp/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── docs/
│   ├── OPENAI_IMAGE_GENERATION.md  # OpenAI API documentation
│   ├── PRD.md                  # Product Requirements Document
│   ├── PRD_CLARIFICATIONS.md   # PRD clarifications
│   └── REPOSITORY_STRUCTURE.md # This file
├── examples/
│   ├── basic_usage.py          # Simple usage example
│   ├── multiple_models.py      # Multi-model example
│   ├── claude_desktop_config.example.json  # Claude Desktop config template
│   ├── README.md               # Examples documentation
│   └── testing/                # Development test scripts (kept for reference)
├── scripts/
│   ├── run_server.py           # Alternative server startup
│   └── start_dev_server.sh     # Development server helper
├── src/
│   └── ai_image_gen_mcp/
│       ├── __init__.py
│       ├── __main__.py         # Package entry point
│       ├── config.py           # Configuration management
│       ├── server.py           # MCP server implementation
│       ├── types.py            # Type definitions
│       ├── models/             # AI model implementations
│       │   ├── __init__.py
│       │   ├── base.py         # Abstract base model
│       │   ├── dalle.py        # DALL-E implementation
│       │   ├── gpt_image.py    # GPT-Image-1 implementation
│       │   └── router.py       # Model routing logic
│       └── storage/            # Storage backends
│           ├── __init__.py
│           ├── base.py         # Abstract storage interface
│           └── local.py        # Local filesystem storage
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_models.py          # Model tests
│   ├── test_server.py          # Server tests
│   └── test_storage.py         # Storage tests
├── .env.example                # Environment configuration template
├── .gitignore                  # Git ignore rules
├── CHANGELOG.md                # Version history
├── CLAUDE.md                   # Claude AI assistant guide
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── README.md                   # Project documentation
├── SETUP_GUIDE.md              # Detailed setup instructions
├── pyproject.toml              # Python project configuration
└── setup.py                    # Setup script for pip install
```

## Key Files

### Configuration
- `.env.example`: Template for environment variables
- `pyproject.toml`: Project metadata and tool configuration

### Documentation
- `README.md`: Main project documentation
- `SETUP_GUIDE.md`: Detailed installation guide
- `CONTRIBUTING.md`: Guidelines for contributors
- `CLAUDE.md`: Instructions for Claude AI assistant

### Source Code
- `server.py`: MCP server with FastMCP
- `models/`: AI model implementations (DALL-E, GPT-Image-1)
- `storage/`: Storage backends (currently local filesystem)

### Examples
- `basic_usage.py`: Simple image generation
- `multiple_models.py`: Using different AI models
- `claude_desktop_config.example.json`: Claude Desktop integration

### CI/CD
- `.github/workflows/ci.yml`: Automated testing and building

## Development Workflow

1. Create virtual environment: `python -m venv .venv`
2. Install dependencies: `pip install -e ".[image,dev]"`
3. Copy `.env.example` to `.env` and add API key
4. Run tests: `pytest`
5. Format code: `black src/ tests/`
6. Lint: `ruff check src/ tests/`
7. Type check: `mypy src/`