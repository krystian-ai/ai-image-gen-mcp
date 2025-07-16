# Contributing to AI Image Generation MCP Server

Thank you for your interest in contributing to the AI Image Generation MCP Server! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Focus on constructive criticism
- Respect differing viewpoints and experiences

## How to Contribute

### Reporting Issues

1. Check if the issue already exists
2. Create a new issue with a clear title and description
3. Include steps to reproduce the problem
4. Add relevant labels (bug, enhancement, documentation, etc.)

### Suggesting Features

1. Open an issue with the "enhancement" label
2. Describe the feature and its use case
3. Explain why this would be valuable to users
4. Be open to discussion and feedback

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`) and ensure they pass
5. Run linting (`black src/ && ruff check src/`)
6. Commit with clear messages (`git commit -m 'Add amazing feature'`)
7. Push to your fork (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- OpenAI API key (for testing)

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/ai-image-gen-mcp.git
cd ai-image-gen-mcp

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[image,dev]"

# Copy environment configuration
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=ai_image_gen_mcp --cov-report=html

# Run specific test file
pytest tests/test_server.py -v
```

### Code Style

We use the following tools to maintain code quality:

- **Black**: Code formatting
- **Ruff**: Linting
- **mypy**: Type checking

Before submitting a PR, run:

```bash
# Format code
black src/ tests/

# Check linting
ruff check src/ tests/

# Type checking
mypy src/
```

### Testing Guidelines

- Write tests for new features
- Maintain or improve code coverage
- Use meaningful test names
- Mock external API calls in unit tests
- Add integration tests for critical paths

## Project Structure

```
ai-image-gen-mcp/
├── src/
│   └── ai_image_gen_mcp/
│       ├── models/        # AI model implementations
│       ├── storage/       # Storage backends
│       ├── server.py      # MCP server
│       └── config.py      # Configuration
├── tests/                 # Test files
├── examples/              # Example scripts
└── docs/                  # Documentation
```

## Adding New Models

To add support for a new AI model:

1. Create a new file in `src/ai_image_gen_mcp/models/`
2. Inherit from `ImageGenerationModel` base class
3. Implement required methods:
   - `generate()`
   - `get_model_info()`
   - `validate_parameters()`
4. Add the model to `ModelRouter` in `router.py`
5. Write tests in `tests/test_models.py`
6. Update documentation

Example:
```python
from .base import ImageGenerationModel

class MyNewModel(ImageGenerationModel):
    async def generate(self, prompt: str, **kwargs) -> list[bytes]:
        # Implementation here
        pass
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions
- Include type hints
- Update CLAUDE.md for development notes

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a release PR
4. After merge, tag the release
5. GitHub Actions will publish to PyPI

## Getting Help

- Open an issue for questions
- Join discussions in the Issues section
- Check existing documentation
- Review closed PRs for examples

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitHub contributors page

Thank you for contributing!