"""Summary-memory overview: maintains compact working context while preserving every original message."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.llm import LLMService
from app.models.models import ConversationSummary
from app.prompts.memory_prompts import SUMMARY_SYSTEM_PROMPT, summary_prompt


class SummaryMemory:
    """Create summaries only after a message threshold, reducing LLM calls and context-window pressure."""

    def get_summary(self, conversation_id: int, db: Session) -> ConversationSummary | None:
        """Return the current compressed context for a session, if one exists."""
        return db.scalar(
            select(ConversationSummary).where(ConversationSummary.conversation_id == conversation_id)
        )

    def update_summary(self, db: Session, conversation_id: int, content: str, message_count: int) -> ConversationSummary:
        """Create or update a summary that records how much history it covers."""
        summary = self.get_summary(conversation_id, db)
        if summary is None:
            summary = ConversationSummary(
                conversation_id=conversation_id, content=content, covered_message_count=message_count
            )
            db.add(summary)
        else:
            summary.content = content
            summary.covered_message_count = message_count
        db.flush()
        return summary

    def generate_summary(self, existing_summary: str | None, messages: list, llm_service: LLMService | None) -> str:
        """Use the configured LLM when available; degrade safely to a concise factual transcript on provider failure."""
        transcript = "\n".join(f"{message.role}: {message.content}" for message in messages)
        if llm_service is not None:
            try:
                return llm_service.generate(
                    summary_prompt(existing_summary, transcript),
                    system_prompt=SUMMARY_SYSTEM_PROMPT,
                    max_tokens=400,
                ).content
            except Exception:
                pass
        recent = messages[-12:]
        return "Recent session facts:\n" + "\n".join(f"{message.role}: {message.content}" for message in recent)
