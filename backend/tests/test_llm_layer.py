"""Offline contract tests for the provider-neutral Phase 7 LLM layer."""

import unittest
from types import SimpleNamespace

from pydantic import ValidationError

from app.llm.exceptions import AuthenticationError, ModelError, RateLimitError
from app.llm.providers.gemini import GeminiProvider
from app.llm.providers.groq import GroqProvider
from app.llm.schemas import LLMMessage, LLMProviderName, LLMRequest


class LLMProviderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.request = LLMRequest(
            messages=[
                LLMMessage(role="system", content="Be concise."),
                LLMMessage(role="user", content="Hello"),
            ],
            max_tokens=20,
        )

    def test_request_requires_messages(self) -> None:
        with self.assertRaises(ValidationError):
            LLMRequest(messages=[])

    def test_gemini_response_is_normalized(self) -> None:
        provider = GeminiProvider("test-key", "gemini-test")
        provider._client = SimpleNamespace(models=SimpleNamespace(generate_content=lambda **_: SimpleNamespace(
            text=" Gemini reply ",
            usage_metadata=SimpleNamespace(prompt_token_count=3, candidates_token_count=2, total_token_count=5),
            candidates=[SimpleNamespace(finish_reason=SimpleNamespace(name="STOP"))],
        )))
        response = provider.chat(self.request)
        self.assertEqual(response.content, "Gemini reply")
        self.assertEqual(response.provider, LLMProviderName.GEMINI)
        self.assertEqual(response.usage.total_tokens, 5)

    def test_groq_response_is_normalized(self) -> None:
        provider = GroqProvider("test-key", "groq-test")
        provider._client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **_: SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=" Groq reply "), finish_reason="stop")],
            usage=SimpleNamespace(prompt_tokens=3, completion_tokens=2, total_tokens=5),
        ))))
        response = provider.chat(self.request)
        self.assertEqual(response.content, "Groq reply")
        self.assertEqual(response.provider, LLMProviderName.GROQ)
        self.assertEqual(response.usage.total_tokens, 5)

    def test_provider_errors_are_standardized(self) -> None:
        self.assertIsInstance(GeminiProvider._translate_error(SimpleNamespace(status_code=401), "model"), AuthenticationError)
        self.assertIsInstance(GroqProvider._translate_error(SimpleNamespace(status_code=429), "model"), RateLimitError)
        self.assertIsInstance(GroqProvider._translate_error(SimpleNamespace(status_code=404), "model"), ModelError)


if __name__ == "__main__":
    unittest.main()
