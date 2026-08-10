"""
Read-only billing tools.

Billing facts must come from the billing system rather than an LLM's memory.
These tools retrieve invoices, payments, and refund status through the billing
service.  They intentionally do not issue refunds or make payment changes;
those are high-impact actions that should use a separately authorized workflow.
"""

from sqlalchemy.orm import Session

from app.services.billing_service import get_billing_by_invoice_number, get_billing_record, search_billing_records
from app.tools.errors import ToolNotFoundError
from app.tools.schemas import BillingToolOutput, InvoiceLookupInput, InvoiceSearchInput


def _billing_output(record) -> BillingToolOutput:
    return BillingToolOutput(
        invoice_id=record.id, customer_id=record.customer_id, invoice_number=record.invoice_number,
        plan=record.plan, amount=record.amount, currency=record.currency, status=record.status,
        record_type=record.record_type, payment_method=record.payment_method, due_date=record.due_date,
        paid_date=record.paid_date, refund_status=record.refund_status,
    )


def get_invoice_tool(db: Session, tool_input: InvoiceLookupInput) -> BillingToolOutput:
    """Retrieve an invoice by internal ID or external invoice number."""
    record = get_billing_record(db, tool_input.invoice_id) if tool_input.invoice_id else get_billing_by_invoice_number(db, tool_input.invoice_number or "")
    if record is None:
        identifier = tool_input.invoice_number or str(tool_input.invoice_id)
        raise ToolNotFoundError(f"Invoice {identifier} was not found.")
    return _billing_output(record)


def search_invoices_tool(db: Session, tool_input: InvoiceSearchInput) -> list[BillingToolOutput]:
    """Find billing records for a customer, invoice number, or plan."""
    return [_billing_output(record) for record in search_billing_records(db, tool_input.customer_id, tool_input.query, tool_input.limit)]


def get_payment_status_tool(db: Session, tool_input: InvoiceLookupInput) -> BillingToolOutput:
    """Return the authoritative payment status for one invoice."""
    return get_invoice_tool(db, tool_input)


def get_refund_status_tool(db: Session, tool_input: InvoiceLookupInput) -> BillingToolOutput:
    """Return the authoritative refund status for one invoice or refund record."""
    return get_invoice_tool(db, tool_input)
