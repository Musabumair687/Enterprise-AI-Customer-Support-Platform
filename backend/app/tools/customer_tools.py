"""
Customer lookup tools.

These read-only tools let an agent ground customer-specific answers in the
database.  For example, an authenticated support workflow can pass its known
customer ID to ``customer_lookup_tool`` before answering a question about plan,
renewal, or support tier.  Authorization belongs to the calling agent/API;
these tools only enforce typed input and reliable service access.
"""

from sqlalchemy.orm import Session

from app.services.customer_service import get_customer, search_customers
from app.tools.errors import ToolNotFoundError
from app.tools.schemas import CustomerLookupInput, CustomerSearchInput, CustomerToolOutput


def _customer_output(customer) -> CustomerToolOutput:
    return CustomerToolOutput(
        customer_id=customer.id, external_id=customer.external_id, name=customer.name,
        email=customer.email, company=customer.company, subscription_plan=customer.subscription_plan,
        status=customer.status, support_tier=customer.support_tier,
        account_manager=customer.account_manager, renewal_date=customer.renewal_date,
    )


def customer_lookup_tool(db: Session, tool_input: CustomerLookupInput) -> CustomerToolOutput:
    """Return one customer's support-relevant account information."""
    customer = get_customer(db, tool_input.customer_id)
    if customer is None:
        raise ToolNotFoundError(f"Customer {tool_input.customer_id} was not found.")
    return _customer_output(customer)


def customer_search_tool(db: Session, tool_input: CustomerSearchInput) -> list[CustomerToolOutput]:
    """Find customers by name, email, or company for an agent's follow-up selection."""
    customers = search_customers(db, tool_input.query, skip=0, limit=tool_input.limit)
    return [_customer_output(customer) for customer in customers]
