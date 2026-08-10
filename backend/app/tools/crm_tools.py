"""
CRM profile tools.

CRM context combines the customer's account facts with recent conversation
history.  This lets a support agent see prior messages without manually joining
database tables in a prompt.  Conversation content can be sensitive, so callers
must authorize access to the customer before invoking this tool.
"""

from sqlalchemy.orm import Session

from app.services.conversation_service import list_customer_conversations
from app.tools.customer_tools import customer_lookup_tool
from app.tools.schemas import ConversationToolOutput, CustomerCRMProfileInput, CustomerCRMProfileOutput, CustomerLookupInput


def get_customer_crm_profile_tool(db: Session, tool_input: CustomerCRMProfileInput) -> CustomerCRMProfileOutput:
    """Return a customer account summary together with their most recent conversations."""
    customer = customer_lookup_tool(db, CustomerLookupInput(customer_id=tool_input.customer_id))
    conversations = list_customer_conversations(db, tool_input.customer_id, tool_input.conversation_limit)
    return CustomerCRMProfileOutput(
        customer=customer,
        recent_conversations=[
            ConversationToolOutput(conversation_id=item.id, ticket_id=item.ticket_id, sender_role=item.sender_role,
                                   content=item.content, created_at=item.created_at)
            for item in conversations
        ],
    )
