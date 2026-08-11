"""Create configured LLM providers without leaking provider setup to callers."""

from app.config import Settings, get_settings
from app.llm.exceptions import UnsupportedProviderError
from app.llm.providers.gemini import GeminiProvider
from app.llm.providers.groq import GroqProvider
from app.llm.schemas import LLMProviderName


def create_provider(provider: LLMProviderName | str, settings: Settings | None = None) -> GeminiProvider | GroqProvider:
    """Build the requested Gemini or Groq provider from validated application settings."""
    configured = settings or get_settings()
    try:
        provider_name = LLMProviderName(provider)
    except ValueError as exc:
        raise UnsupportedProviderError(f"Unsupported LLM provider: {provider}") from exc
    if provider_name is LLMProviderName.GEMINI:
        return GeminiProvider(configured.gemini_api_key, configured.gemini_model, configured.llm_timeout_seconds)
    return GroqProvider(configured.groq_api_key, configured.groq_model, configured.llm_timeout_seconds)
