"""The fixed vocabulary used for customer-support intent classification."""

from enum import StrEnum


class Intent(StrEnum):
    """Business intents supported by the Phase 9 classifier."""

    BILLING = "billing"
    TECHNICAL_SUPPORT = "technical_support"
    GENERAL_QUESTION = "general_question"
    REFUND = "refund"
    SALES = "sales"
    HUMAN_AGENT = "human_agent"
    FEATURE_REQUEST = "feature_request"
    COMPLAINT = "complaint"
