"""Configuration management for the AI Image Generation MCP Server."""

import os
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv


class Config(BaseModel):
    """Server configuration."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(
        ...,
        description="OpenAI API key for GPT-Image-1"
    )
    
    # Model Configuration
    model_default: str = Field(
        default="gpt-4.1-mini",
        description="Default model to use"
    )
    model_provider: str = Field(
        default="openai",
        description="Model provider"
    )
    
    # Storage Configuration
    cache_dir: Path = Field(
        default=Path("/tmp/ai-image-gen-cache"),
        description="Directory for storing generated images"
    )
    storage_type: str = Field(
        default="local",
        description="Storage backend type"
    )
    
    # Server Configuration
    server_name: str = Field(
        default="AI Image Generation MCP Server",
        description="Server name for identification"
    )
    server_version: str = Field(
        default="0.1.0",
        description="Server version"
    )
    
    # Logging
    log_level: str = Field(
        default="INFO",
        description="Logging level"
    )
    
    # Rate Limiting
    rate_limit_rpm: int = Field(
        default=60,
        description="Rate limit in requests per minute"
    )
    
    # Development
    debug: bool = Field(
        default=False,
        description="Debug mode"
    )
    
    @validator("cache_dir", pre=True)
    def expand_cache_dir(cls, v):
        """Expand cache directory path."""
        if isinstance(v, str):
            v = Path(v).expanduser().resolve()
        return v
    
    @validator("openai_api_key")
    def validate_api_key(cls, v):
        """Validate OpenAI API key format."""
        if not v or not v.startswith("sk-"):
            raise ValueError("Invalid OpenAI API key format")
        return v
    
    class Config:
        """Pydantic config."""
        case_sensitive = False
        env_prefix = ""


def load_config(env_file: Optional[Path] = None) -> Config:
    """Load configuration from environment variables and .env file."""
    if env_file is None:
        env_file = Path(".env")
    
    if env_file.exists():
        load_dotenv(env_file)
    
    # Load from environment variables
    config_data = {
        "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
        "model_default": os.getenv("MODEL_DEFAULT", "gpt-4.1-mini"),
        "model_provider": os.getenv("MODEL_PROVIDER", "openai"),
        "cache_dir": os.getenv("CACHE_DIR", "/tmp/ai-image-gen-cache"),
        "storage_type": os.getenv("STORAGE_TYPE", "local"),
        "server_name": os.getenv("SERVER_NAME", "AI Image Generation MCP Server"),
        "server_version": os.getenv("SERVER_VERSION", "0.1.0"),
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "rate_limit_rpm": int(os.getenv("RATE_LIMIT_RPM", "60")),
        "debug": os.getenv("DEBUG", "false").lower() == "true",
    }
    
    return Config(**config_data)