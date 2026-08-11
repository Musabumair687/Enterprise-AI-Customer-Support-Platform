"""Standardized failures raised by the provider-neutral LLM layer."""


class LLMError(Exception):
    """Base class for expected LLM-layer failures."""


class ProviderError(LLMError):
    """Raised when a provider returns an unexpected service error."""


class AuthenticationError(ProviderError):
    """Raised when a provider rejects the configured API key."""


class RateLimitError(ProviderError):
    """Raised when a provider temporarily limits requests."""


class ModelError(ProviderError):
    """Raised when a requested model is invalid or unavailable."""


class LLMTimeoutError(ProviderError):
    """Raised when an LLM request exceeds the configured deadline."""



class UnsupportedProviderError(LLMError):
    """Raised when a caller asks for a provider outside Gemini and Groq."""
