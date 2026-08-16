"""Memory-manager overview: the single graph-facing interface for sessions, messages, summaries, and durable memories."""

from collections.abc import Callable

from langchain_core.messages import HumanMessage
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.llm import LLMService
from app.memory.conversation_memory import ConversationMemory
from app.memory.long_term_memory import LongTermMemory
from app.memory.memory_retriever import MemoryRetriever
from app.memory.session_memory import SessionMemory
from app.memory.summary_memory import SummaryMemory
from app.models.models import Customer, ConversationSession
from app.schemas.memory import MemoryCandidate, MemoryContext, MemoryMessage
from app.state.chat_state import ChatState


class MemoryManager:
    """Keep all memory persistence and retrieval policy out of individual agents and graph nodes."""

    def __init__(
        self,
        session_factory: Callable[[], Session] = SessionLocal,
        llm_service: LLMService | None = None,
        summary_threshold: int = 15,
    ) -> None:
        self.session_factory = session_factory
        self.llm_service = llm_service or LLMService()
        self.summary_threshold = summary_threshold
        self.conversations = ConversationMemory()
        self.sessions = SessionMemory()
        self.summaries = SummaryMemory()
        self.long_term = LongTermMemory()
        self.retriever = MemoryRetriever()

    def load_context(self, customer_id: int, session_id: str, query: str) -> MemoryContext:
        """Create/load a session and return only the memory needed for the next graph execution."""
        with self.session_factory() as db:
            if db.get(Customer, customer_id) is None:
                raise ValueError(f"Customer {customer_id} was not found.")
            conversation = self.sessions.get_or_create_session(db, customer_id, session_id)
            summary = self.summaries.get_summary(conversation.id, db)
            recent_messages = self.conversations.get_recent_messages(db, conversation.id)
            relevant_memories = self.retriever.retrieve(
                query, self.long_term.get_customer_memories(db, customer_id)
            )
            context = MemoryContext(
                conversation_id=conversation.id,
                session_id=conversation.session_id,
                summary=summary.content if summary else None,
                recent_messages=[MemoryMessage.model_validate(message) for message in recent_messages],
                long_term_memories=[
                    MemoryCandidate(
                        memory_type=memory.memory_type,
                        content=memory.content,
                        importance=memory.importance,
                        metadata=memory.memory_metadata or {},
                    )
                    for memory in relevant_memories
                ],
                session_memory={
                    "intent": conversation.current_intent,
                    "product": conversation.current_product,
                    "issue": conversation.current_issue,
                    "ticket": conversation.current_ticket,
                    "status": conversation.status,
                },
            )
            db.commit()
            return context

    def record_turn(
        self,
        customer_id: int,
        session_id: str,
        user_message: str,
        assistant_message: str,
        *,
        intent: str | None = None,
        product: str | None = None,
        issue: str | None = None,
        ticket: str | None = None,
        turn_id: str | None = None,
    ) -> ConversationSession:
        """Persist both sides of a completed turn, then summarize only when the threshold is crossed."""
        with self.session_factory() as db:
            conversation = self.sessions.get_or_create_session(db, customer_id, session_id)
            self.sessions.update_context(
                conversation,
                current_intent=intent,
                current_product=product,
                current_issue=issue,
                current_ticket=ticket,
            )
            self.conversations.save_message(db, conversation.id, "user", user_message, turn_id=turn_id)
            self.conversations.save_message(db, conversation.id, "assistant", assistant_message, turn_id=turn_id)
            messages = self.conversations.get_messages(db, conversation.id)
            existing_summary = self.summaries.get_summary(conversation.id, db)
            if len(messages) > self.summary_threshold and (
                existing_summary is None or existing_summary.covered_message_count < len(messages)
            ):
                content = self.summaries.generate_summary(
                    existing_summary.content if existing_summary else None, messages, self.llm_service
                )
                self.summaries.update_summary(db, conversation.id, content, len(messages))
            db.commit()
            return conversation

    def save_long_term_memory(self, customer_id: int, candidate: MemoryCandidate) -> None:
        """Store a policy-validated durable fact in its own short transaction."""
        with self.session_factory() as db:
            if db.get(Customer, customer_id) is None:
                raise ValueError(f"Customer {customer_id} was not found.")
            self.long_term.save_memory(db, customer_id, candidate)
            db.commit()

    def load_graph_state(self, state: ChatState) -> dict[str, object]:
        """LangGraph node: inject persistent context before intent classification and agent selection."""
        customer_id = state.get("customer_id")
        if customer_id is None:
            return {"conversation_id": None, "conversation_summary": None, "long_term_memories": [], "session_memory": {}}
        message = next(
            (
                item.content.strip()
                for item in reversed(state.get("messages", []))
                if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()
            ),
            "",
        )
        context = self.load_context(customer_id, state["session_id"], message)
        return {
            "conversation_id": context.conversation_id,
            "conversation_summary": context.summary,
            "recent_messages": [message.model_dump() for message in context.recent_messages],
            "long_term_memories": [memory.model_dump() for memory in context.long_term_memories],
            "session_memory": context.session_memory,
        }

    def save_graph_state(self, state: ChatState) -> dict[str, object]:
        """LangGraph node: persist the completed turn after the specialized agent creates its response."""
        customer_id = state.get("customer_id")
        response = state.get("response")
        if customer_id is None or not response:
            return {}
        user_message = next(
            (
                item.content.strip()
                for item in reversed(state.get("messages", []))
                if isinstance(item, HumanMessage) and isinstance(item.content, str) and item.content.strip()
            ),
            "",
        )
        if user_message:
            session_memory = state.get("session_memory", {})
            self.record_turn(
                customer_id,
                state["session_id"],
                user_message,
                response,
                intent=str(state["intent"].value) if state.get("intent") else None,
                product=str(session_memory.get("product") or "") or None,
                issue=str(session_memory.get("issue") or "") or None,
                ticket=str(session_memory.get("ticket") or "") or None,
                turn_id=state.get("turn_id"),
            )
        return {}

    @staticmethod
    def format_context(state: ChatState) -> str:
        """Format bounded memory for an agent system prompt without exposing raw database objects."""
        blocks: list[str] = []
        if state.get("conversation_summary"):
                blocks.append(f"Conversation summary:\n{state['conversation_summary']}")
        recent_messages = state.get("recent_messages", [])
        if recent_messages:
            blocks.append(
                "Recent conversation messages:\n"
                + "\n".join(f"- {item['role']}: {item['content']}" for item in recent_messages[-10:])
            )
        if state.get("session_memory"):
            useful = {key: value for key, value in state["session_memory"].items() if value}
            if useful:
                blocks.append("Current session facts:\n" + "\n".join(f"- {key}: {value}" for key, value in useful.items()))
        memories = state.get("long_term_memories", [])
        if memories:
            blocks.append("Relevant durable customer facts:\n" + "\n".join(f"- {item['content']}" for item in memories))
        return "\n\n".join(blocks)
