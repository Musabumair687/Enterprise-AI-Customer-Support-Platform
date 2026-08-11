"""Provider-neutral contracts for the LLM layer."""

from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class LLMProviderName(StrEnum):
    """The only hosted LLM providers supported by this application."""

    GEMINI = "gemini"
    GROQ = "groq"


class LLMMessage(BaseModel):
    """A single conversation turn passed to either provider."""

    role: Literal["system", "user", "assistant"]
    content: str = Field(min_length=1)


class LLMRequest(BaseModel):
    """A validated, provider-neutral chat-completion request."""

    messages: list[LLMMessage] = Field(min_length=1)
    provider: LLMProviderName | None = None
    model: str | None = Field(default=None, min_length=1)
    temperature: float = Field(default=0.2, ge=0, le=2)
    max_tokens: int = Field(default=1_024, ge=1, le=32_768)
    timeout_seconds: float | None = Field(default=None, gt=0, le=300)


class LLMUsage(BaseModel):
    """Normalized token counts when the provider reports them."""

    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)


class LLMResponse(BaseModel):
    """Provider-neutral text response and execution metadata."""

    model_config = ConfigDict(frozen=True)

    content: str
    provider: LLMProviderName
    model: str
    usage: LLMUsage
    finish_reason: str | None
    latency_ms: float = Field(ge=0)
