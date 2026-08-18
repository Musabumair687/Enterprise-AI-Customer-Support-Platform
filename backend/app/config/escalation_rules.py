"""Deterministic policy for deciding when a support turn needs a human."""

from __future__ import annotations

import re


LOW_CONFIDENCE_THRESHOLD = 0.5
RETRY_CONFIDENCE_THRESHOLD = 0.8
HUMAN_REQUEST_TERMS = ("human", "live agent", "representative", "manager", "speak to someone")
SENSITIVE_PATTERNS = {
    "security": ("security breach", "hacked", "data breach", "unauthorized access", "account compromised"),
    "legal": ("legal", "lawyer", "sue", "lawsuit", "gdpr", "data deletion"),
    "billing": ("refund", "chargeback", "charged"),
}
LARGE_REFUND_PATTERN = re.compile(r"\$\s*(?:[1-9]\d{3,}|\d{1,3}(?:,\d{3})+)")


def escalation_reason(message: str, confidence_score: float, failed_attempts: int = 0) -> str | None:
    """Return the policy reason for escalation, or ``None`` when AI may answer."""
    text = message.casefold()
    if any(term in text for term in HUMAN_REQUEST_TERMS):
        return "The customer explicitly requested human assistance."
    for category, patterns in SENSITIVE_PATTERNS.items():
        if any(pattern in text for pattern in patterns):
            if category != "billing" or LARGE_REFUND_PATTERN.search(message):
                return f"This is a sensitive {category} matter that requires human review."
    if failed_attempts >= 3:
        return "The issue has not been resolved after repeated AI attempts."
    if confidence_score < LOW_CONFIDENCE_THRESHOLD:
        return "AI confidence is below the safe response threshold."
    return None


def classify_department(message: str) -> str:
    """Choose the owning team from a minimal, auditable keyword policy."""
    text = message.casefold()
    if any(term in text for term in ("refund", "invoice", "charged", "payment", "billing")):
        return "Finance"
    if any(term in text for term in ("security", "breach", "hacked", "legal", "lawyer", "lawsuit")):
        return "Security"
    if any(term in text for term in ("angry", "manager", "complaint", "destroyed my business")):
        return "Customer Success"
    return "Technical Support"


def classify_priority(message: str) -> str:
    """Derive a conservative ticket priority for a human handoff."""
    text = message.casefold()
    if any(term in text for term in ("security breach", "hacked", "lawsuit", "urgent", "immediate", "destroyed my business")):
        return "urgent"
    if any(term in text for term in ("refund", "charged", "not working", "failing", "complaint")):
        return "high"
    return "medium"
