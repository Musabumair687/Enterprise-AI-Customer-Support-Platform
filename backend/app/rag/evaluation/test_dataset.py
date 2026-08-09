"""Small, versioned seed set for retrieval regression checks."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RetrievalTestCase:
    question: str
    expected_documents: tuple[str, ...]


TEST_CASES = (
    RetrievalTestCase("How can I reset my CloudDesk password?", ("clouddesk-chat-user-manual.md",)),
    RetrievalTestCase("What is the refund policy?", ("corvex-cloud-refund-policy.md",)),
    RetrievalTestCase("How do I troubleshoot CloudDesk mobile?", ("clouddesk-mobile-troubleshooting-guide.md",)),
)
