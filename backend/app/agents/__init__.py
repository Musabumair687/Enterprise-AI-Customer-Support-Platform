"""Phase 10 specialized agents with least-privilege tool declarations."""
from app.agents.billing_agent import BillingAgent
from app.agents.customer_agent import CustomerAgent
from app.agents.technical_agent import TechnicalAgent
from app.agents.product_agent import ProductAgent
from app.agents.escalation_agent import EscalationAgent
from app.agents.sales_agent import SalesAgent
from app.agents.supervisor import SupervisorAgent
__all__ = ["BillingAgent", "CustomerAgent", "TechnicalAgent", "ProductAgent", "EscalationAgent", "SalesAgent", "SupervisorAgent"]
