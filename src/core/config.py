"""Configuration module for the AI-Powered Interactive Coding Tutor."""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = "your_openai_api_key_here"
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 500
    openai_temperature: float = 0.7
    
    # Application Configuration
    app_name: str = "AI-Powered Interactive Coding Tutor"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # API Configuration
    api_rate_limit: int = 100
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
