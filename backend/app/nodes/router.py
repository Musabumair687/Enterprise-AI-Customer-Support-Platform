"""LLM-backed, structured intent classification for the first LangGraph node."""

import json
import re
from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage

from app.config import Settings, get_settings
from app.core.logging import get_logger
from app.llm import LLMMessage, LLMProviderName, LLMRequest, LLMService
from app.prompts.router_prompts import ROUTER_SYSTEM_PROMPT, ROUTES
from app.state.chat_state import ChatState, Route


class RouterNode:
    """Classify the latest customer message and update only the graph route."""

    def __init__(self, llm_service: LLMService | None = None, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.llm_service = llm_service or LLMService(self.settings)
        self.logger = get_logger()

    def __call__(self, state: ChatState) -> dict[str, Route]:
        message = self._latest_customer_message(state["messages"])
        if message is None:
            self.logger.warning("Router received no non-empty customer message; route=unknown")
            return {"route": "unknown"}

        try:
            response = self.llm_service.chat(
                LLMRequest(
                    messages=[
                        LLMMessage(role="system", content=ROUTER_SYSTEM_PROMPT),
                        LLMMessage(role="user", content=message),
                    ],
                    provider=LLMProviderName(self.settings.router_llm_provider),
                    temperature=0,
                    # Gemini reasoning models may consume part of the output
                    # budget before emitting the tiny JSON classification.
                    max_tokens=256,
                )
            )
            route = parse_route(response.content)
            self.logger.info(
                "Route decided | session_id=%s route=%s provider=%s model=%s latency_ms=%.2f",
                state["session_id"], route, response.provider, response.model, response.latency_ms,
            )
            return {"route": route}
        except Exception:
            self.logger.exception("Routing failed | session_id=%s; route=unknown", state["session_id"])
            return {"route": "unknown"}

    @staticmethod
    def _latest_customer_message(messages: list[BaseMessage]) -> str | None:
        for message in reversed(messages):
            if isinstance(message, HumanMessage) and isinstance(message.content, str):
                content = message.content.strip()
                if content:
                    return content
        return None


def parse_route(content: str) -> Route:
    """Accept only an allowed structured LLM route; malformed output becomes unknown."""
    try:
        payload: Any = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{\s*\"route\"\s*:\s*\"([^\"]+)\"\s*\}", content)
        payload = {"route": match.group(1)} if match else {}
    route = payload.get("route") if isinstance(payload, dict) else None
    return route if route in ROUTES else "unknown"
