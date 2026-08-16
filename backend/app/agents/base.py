"""Shared safe response behavior for Phase 10 specialized agents."""

from langchain_core.messages import HumanMessage

from app.core.logging import get_logger
from app.llm import LLMService
from app.memory.memory_manager import MemoryManager
from app.state.chat_state import ChatState


class SpecializedAgent:
    """A narrowly scoped response agent; subclasses declare their prompt and tool allow-list."""

    name: str
    system_prompt: str
    allowed_tools: frozenset[str]

    def __init__(self, llm_service: LLMService | None = None) -> None:
        self.llm_service = llm_service or LLMService()
        self.logger = get_logger()

    def __call__(self, state: ChatState) -> dict[str, object]:
        message = next((item.content.strip() for item in reversed(state["messages"])
                        if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()), "")
        if not message:
            return {"agent": self.name, "response": "Please share your question so I can help.",
                    "metadata": {**state.get("metadata", {}), "agent_status": "empty_message"}}
        try:
            memory_context = MemoryManager.format_context(state)
            system_prompt = f"{self.system_prompt}\n\n{memory_context}" if memory_context else self.system_prompt
            response = self.llm_service.generate(message, system_prompt=system_prompt, max_tokens=512)
        except Exception:
            self.logger.warning("Specialized agent unavailable | session_id=%s agent=%s", state["session_id"], self.name)
            return {"agent": self.name,
                    "response": "I'm sorry, I couldn't complete that request right now. Please try again shortly.",
                    "metadata": {**state.get("metadata", {}), "agent_status": "provider_error",
                                 "allowed_tools": sorted(self.allowed_tools)}}
        return {"agent": self.name, "response": response.content,
                "metadata": {**state.get("metadata", {}), "agent_status": "success",
                             "allowed_tools": sorted(self.allowed_tools)}}
