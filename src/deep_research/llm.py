from __future__ import annotations

from typing import Optional
from langchain_openai import ChatOpenAI
from deep_research.config import get_settings

settings = get_settings()


def create_groq_llm(model_name: Optional[str] = None, temperature: float = 0.2) -> ChatOpenAI:
    """Create a Groq ChatOpenAI client (Ultra-fast LPU inference)."""
    target_model = model_name or settings.groq_model
    kwargs = {
        "model": target_model,
        "api_key": settings.groq_api_key,
        "base_url": settings.groq_base_url,
        "temperature": temperature,
        "timeout": settings.timeout_seconds,
        "max_retries": 1,
        "default_headers": {"User-Agent": "Mozilla/5.0"}
    }
    # Groq on-demand enforces a 1000 OTPM limit on qwen preview models
    if "qwen" in target_model.lower():
        kwargs["max_tokens"] = 950
    return ChatOpenAI(**kwargs)


def create_nvidia_llm(model_name: Optional[str] = None, temperature: float = 0.2) -> ChatOpenAI:
    """Create an NVIDIA NIM ChatOpenAI client (550B flagship reasoning)."""
    target_model = model_name or settings.nvidia_model
    return ChatOpenAI(
        model=target_model,
        api_key=settings.nvidia_api_key,
        base_url=settings.nvidia_base_url,
        temperature=temperature,
        timeout=settings.timeout_seconds,
        max_retries=2,
    )


def get_llm(
    provider: Optional[str] = None,
    model_name: Optional[str] = None,
    temperature: float = 0.2,
    enable_fallback: bool = True
):
    """Return an LLM instance with automatic cross-provider fallback.
    
    If primary provider (e.g. NVIDIA) encounters timeout or failure,
    it automatically falls back to Groq (or vice versa).
    """
    active_provider = (provider or settings.default_provider).lower()

    if active_provider == "groq":
        primary = create_groq_llm(model_name, temperature)
        if enable_fallback and settings.nvidia_api_key:
            fallback = create_nvidia_llm(temperature=temperature)
            return primary.with_fallbacks([fallback])
        return primary

    # Default to NVIDIA NIM with Groq as ultra-fast fallback
    primary = create_nvidia_llm(model_name, temperature)
    if enable_fallback and settings.groq_api_key:
        fallback = create_groq_llm(model_name=settings.groq_model, temperature=temperature)
        return primary.with_fallbacks([fallback])
    return primary
