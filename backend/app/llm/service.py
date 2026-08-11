"""Application-facing interface for Gemini and Groq chat generation."""

from app.config import Settings, get_settings
from app.llm.factory import create_provider
from app.llm.schemas import LLMMessage, LLMProviderName, LLMRequest, LLMResponse


class LLMService:
    """Route provider-neutral requests to the configured Gemini or Groq implementation."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._providers: dict[LLMProviderName, object] = {}

    def chat(self, request: LLMRequest) -> LLMResponse:
        """Complete a conversation through the requested or default provider."""
        provider_name = request.provider or LLMProviderName(self.settings.default_llm_provider)
        provider = self._providers.get(provider_name)
        if provider is None:
            provider = create_provider(provider_name, self.settings)
            self._providers[provider_name] = provider
        return provider.chat(request)  # type: ignore[union-attr]

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        provider: LLMProviderName | None = None,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 1_024,
    ) -> LLMResponse:
        """Convenience API for a single user prompt, optionally with a system instruction."""
        messages = ([LLMMessage(role="system", content=system_prompt)] if system_prompt else [])
        messages.append(LLMMessage(role="user", content=prompt))
        return self.chat(LLMRequest(messages=messages, provider=provider, model=model,
                                    temperature=temperature, max_tokens=max_tokens))
