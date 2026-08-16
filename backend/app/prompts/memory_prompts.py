"""Prompt overview: bounded instructions used only when an LLM summarizes an existing support session."""


SUMMARY_SYSTEM_PROMPT = """Summarize this customer-support session for a future support agent. Preserve product names,
error codes, completed troubleshooting, open tickets, customer preferences, and unresolved next steps. Do not invent facts."""


def summary_prompt(existing_summary: str | None, transcript: str) -> str:
    """Build a concise summarization request while retaining earlier summary context."""
    prior = existing_summary or "No earlier summary exists."
    return f"Existing summary:\n{prior}\n\nNew conversation messages:\n{transcript}"
