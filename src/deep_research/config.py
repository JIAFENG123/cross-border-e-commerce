from __future__ import annotations

import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Provider selection
    default_provider: str = Field(
        default="groq",
        alias="DEFAULT_PROVIDER",
        description="Active provider: 'groq' or 'nvidia'"
    )

    # Groq Settings (Ultra-Fast Inference)
    groq_api_key: str = Field(
        default="",
        alias="GROQ_API_KEY",
        description="Groq API key"
    )
    groq_base_url: str = Field(
        default="https://api.groq.com/openai/v1",
        alias="GROQ_BASE_URL",
        description="Groq OpenAI-compatible base URL"
    )
    groq_model: str = Field(
        default="openai/gpt-oss-120b",
        alias="GROQ_MODEL",
        description="Default fast Groq model"
    )
    groq_model_reasoning: str = Field(
        default="openai/gpt-oss-120b",
        alias="GROQ_MODEL_REASONING",
        description="High-reasoning Groq model"
    )
    groq_model_fast: str = Field(
        default="openai/gpt-oss-20b",
        alias="GROQ_MODEL_FAST",
        description="Fast Groq parsing model"
    )

    # NVIDIA NIM Settings (Ultra-Large 550B)
    nvidia_api_key: str = Field(
        default="",
        alias="NVIDIA_API_KEY",
        description="NVIDIA NIM API key"
    )
    nvidia_base_url: str = Field(
        default="https://integrate.api.nvidia.com/v1",
        alias="NVIDIA_BASE_URL",
        description="NVIDIA NIM base URL"
    )
    nvidia_model: str = Field(
        default="nvidia/nemotron-3-ultra-550b-a55b",
        alias="NVIDIA_MODEL",
        description="NVIDIA 550B flagship model"
    )
    nvidia_model_fast: str = Field(
        default="nvidia/nemotron-3.5-bolt-e4b",
        alias="NVIDIA_MODEL_FAST",
        description="Fast NVIDIA model"
    )

    # Backward compatibility
    llm_model: str = Field(
        default="nvidia/nemotron-3-ultra-550b-a55b",
        alias="LLM_MODEL"
    )

    max_research_iterations: int = Field(default=1, alias="MAX_RESEARCH_ITERATIONS")
    default_target_market: str = Field(default="US", alias="DEFAULT_TARGET_MARKET")
    timeout_seconds: float = Field(default=60.0, alias="TIMEOUT_SECONDS")


@lru_cache
def get_settings() -> Settings:
    return Settings()
