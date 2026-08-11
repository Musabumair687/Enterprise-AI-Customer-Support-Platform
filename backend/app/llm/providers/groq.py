"""Groq-specific implementation hidden behind the common LLM contracts."""

from time import perf_counter
from typing import Any

from app.llm.exceptions import AuthenticationError, LLMTimeoutError, ModelError, ProviderError, RateLimitError
from app.llm.schemas import LLMProviderName, LLMRequest, LLMResponse, LLMUsage


class GroqProvider:
    """Generate text with Groq's chat-completions API."""

    provider_name = LLMProviderName.GROQ

    def __init__(self, api_key: str, model: str, timeout_seconds: float = 60.0) -> None:
        try:
            from groq import Groq
        except ImportError as exc:
            raise ProviderError("Groq SDK is not installed. Install the backend requirements.") from exc
        self.model = model
        self.timeout_seconds = timeout_seconds
        self._client = Groq(api_key=api_key, timeout=timeout_seconds)

    def chat(self, request: LLMRequest) -> LLMResponse:
        """Send a multi-turn conversation to Groq."""
        model = request.model or self.model
        started = perf_counter()
        try:
            response = self._client.chat.completions.create(
                model=model,
                messages=[message.model_dump() for message in request.messages],
                temperature=request.temperature,
                max_completion_tokens=request.max_tokens,
                timeout=request.timeout_seconds or self.timeout_seconds,
            )
        except Exception as exc:
            raise self._translate_error(exc, model) from exc
        latency_ms = (perf_counter() - started) * 1_000
        usage = getattr(response, "usage", None)
        choice = response.choices[0] if response.choices else None
        content = getattr(getattr(choice, "message", None), "content", None) or ""
        return LLMResponse(
            content=content.strip(),
            provider=self.provider_name,
            model=model,
            usage=LLMUsage(
                input_tokens=getattr(usage, "prompt_tokens", None),
                output_tokens=getattr(usage, "completion_tokens", None),
                total_tokens=getattr(usage, "total_tokens", None),
            ),
            finish_reason=getattr(choice, "finish_reason", None),
            latency_ms=latency_ms,
        )

    @staticmethod
    def _translate_error(error: Exception, model: str) -> ProviderError:
        status_code = getattr(error, "status_code", None)
        if status_code in {401, 403}:
            return AuthenticationError("Groq authentication failed.")
        if status_code == 429:
            return RateLimitError("Groq rate limit reached.")
        if status_code in {400, 404}:
            return ModelError(f"Groq model '{model}' is unavailable or invalid.")
        if isinstance(error, TimeoutError) or "timeout" in type(error).__name__.lower():
            return LLMTimeoutError("Groq request timed out.")
        return ProviderError("Groq request failed.")
