"""Gemini-specific implementation hidden behind the common LLM contracts."""

from time import perf_counter
from typing import Any

from google import genai
from google.genai import types

from app.llm.exceptions import AuthenticationError, LLMTimeoutError, ModelError, ProviderError, RateLimitError
from app.llm.schemas import LLMMessage, LLMProviderName, LLMRequest, LLMResponse, LLMUsage


class GeminiProvider:
    """Generate text with Gemini while returning application-level response objects."""

    provider_name = LLMProviderName.GEMINI

    def __init__(self, api_key: str, model: str, timeout_seconds: float = 60.0) -> None:
        self.model = model
        self.timeout_seconds = timeout_seconds
        self._client = genai.Client(api_key=api_key)

    def chat(self, request: LLMRequest) -> LLMResponse:
        """Send a multi-turn conversation to Gemini."""
        model = request.model or self.model
        system_instruction, contents = self._to_gemini_contents(request.messages)
        started = perf_counter()
        try:
            response = self._client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction or None,
                    temperature=request.temperature,
                    max_output_tokens=request.max_tokens,
                    http_options=types.HttpOptions(timeout=int((request.timeout_seconds or self.timeout_seconds) * 1_000)),
                ),
            )
        except Exception as exc:
            raise self._translate_error(exc, model) from exc
        latency_ms = (perf_counter() - started) * 1_000
        usage = getattr(response, "usage_metadata", None)
        candidate = response.candidates[0] if getattr(response, "candidates", None) else None
        return LLMResponse(
            content=(getattr(response, "text", None) or "").strip(),
            provider=self.provider_name,
            model=model,
            usage=LLMUsage(
                input_tokens=getattr(usage, "prompt_token_count", None),
                output_tokens=getattr(usage, "candidates_token_count", None),
                total_tokens=getattr(usage, "total_token_count", None),
            ),
            finish_reason=self._enum_value(getattr(candidate, "finish_reason", None)),
            latency_ms=latency_ms,
        )

    @staticmethod
    def _to_gemini_contents(messages: list[LLMMessage]) -> tuple[str, list[types.Content]]:
        system_parts = [message.content for message in messages if message.role == "system"]
        contents = [
            types.Content(role="model" if message.role == "assistant" else "user", parts=[types.Part(text=message.content)])
            for message in messages
            if message.role != "system"
        ]
        if not contents:
            raise ProviderError("Gemini requests require at least one user or assistant message.")
        return "\n\n".join(system_parts), contents

    @staticmethod
    def _enum_value(value: Any) -> str | None:
        return getattr(value, "name", None) or (str(value) if value is not None else None)

    @staticmethod
    def _translate_error(error: Exception, model: str) -> ProviderError:
        status_code = getattr(error, "code", None) or getattr(error, "status_code", None)
        if status_code in {401, 403}:
            return AuthenticationError("Gemini authentication failed.")
        if status_code == 429:
            return RateLimitError("Gemini rate limit reached.")
        if status_code in {404, 400}:
            return ModelError(f"Gemini model '{model}' is unavailable.")
        if isinstance(error, TimeoutError) or "timeout" in type(error).__name__.lower():
            return LLMTimeoutError("Gemini request timed out.")
        return ProviderError("Gemini request failed.")
