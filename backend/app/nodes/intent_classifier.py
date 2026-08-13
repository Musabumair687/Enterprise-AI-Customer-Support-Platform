"""Structured, LLM-backed classification of the latest customer-support intent."""

import json
import re
from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage

from app.config import Settings, get_settings
from app.core.logging import get_logger
from app.llm import LLMMessage, LLMProviderName, LLMRequest, LLMService
from app.prompts.intent_prompts import INTENT_SYSTEM_PROMPT
from app.schemas.intent import Intent
from app.state.chat_state import ChatState


class IntentClassifierNode:
    """Classify one conversation's latest customer message without solving it."""

    def __init__(self, llm_service: LLMService | None = None, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.llm_service = llm_service or LLMService(self.settings)
        self.logger = get_logger()

    def __call__(self, state: ChatState) -> dict[str, Intent | None | dict[str, str | float | int | None]]:
        message = self._latest_customer_message(state["messages"])
        if message is None:
            self.logger.warning("Intent classification skipped | session_id=%s reason=empty_message", state["session_id"])
            return {"intent": None, "metadata": {"classification_status": "empty_message"}}
        try:
            response = self.llm_service.chat(LLMRequest(
                messages=[LLMMessage(role="system", content=INTENT_SYSTEM_PROMPT), LLMMessage(role="user", content=message)],
                provider=LLMProviderName(self.settings.intent_llm_provider), temperature=0, max_tokens=256,
            ))
            intent = parse_intent(response.content)
            status = "success" if intent is not None else "invalid_intent"
            metadata = {"classification_status": status, "provider": str(response.provider), "model": response.model, "latency_ms": response.latency_ms}
            self.logger.info("Intent classified | session_id=%s intent=%s provider=%s model=%s latency_ms=%.2f", state["session_id"], intent, response.provider, response.model, response.latency_ms)
            return {"intent": intent, "metadata": metadata}
        except Exception:
            self.logger.exception("Intent classification failed | session_id=%s", state["session_id"])
            return {"intent": None, "metadata": {"classification_status": "provider_error"}}

    @staticmethod
    def _latest_customer_message(messages: list[BaseMessage]) -> str | None:
        for message in reversed(messages):
            if isinstance(message, HumanMessage) and isinstance(message.content, str) and message.content.strip():
                return message.content.strip()
        return None


def parse_intent(content: str) -> Intent | None:
    """Return a valid intent only when the provider supplied a permitted structured value."""
    try:
        payload: Any = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{\s*\"intent\"\s*:\s*\"([^\"]+)\"\s*\}", content)
        payload = {"intent": match.group(1)} if match else {}
    try:
        return Intent(payload.get("intent")) if isinstance(payload, dict) else None
    except (TypeError, ValueError):
        return None
