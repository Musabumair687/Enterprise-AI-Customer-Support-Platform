"""Central, policy-aware catalogue of tools exposed to future LangGraph agents."""

from collections.abc import Callable
from dataclasses import dataclass
import logging
from time import perf_counter
from typing import Any

from app.tools.billing_tools import get_invoice_tool, get_payment_status_tool, get_refund_status_tool, search_invoices_tool
from app.tools.crm_tools import get_customer_crm_profile_tool
from app.tools.customer_tools import customer_lookup_tool, customer_search_tool
from app.tools.employee_tools import find_employee_by_skill_tool, find_employee_tool, find_support_agent_tool
from app.tools.errors import ToolError, ToolOperationError, ToolPermissionDeniedError
from app.tools.escalation_tools import assign_ticket_tool, escalate_ticket_tool
from app.tools.known_issue_tools import search_known_issues_tool
from app.tools.product_tools import get_product_tool, list_products_tool
from app.tools.rag_tools import knowledge_base_search_tool
from app.tools.ticket_tools import create_ticket_tool, get_ticket_tool, search_tickets_tool, update_ticket_tool


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """Tool callable plus the policy information used by agent orchestration."""
    name: str
    description: str
    handler: Callable[..., Any]
    read_only: bool
    requires_confirmation: bool
    allowed_agents: frozenset[str]


ALL_AGENTS = frozenset({"billing_agent", "customer_agent", "technical_agent", "product_agent", "escalation_agent", "sales_agent"})
logger = logging.getLogger(__name__)


def _tool(name: str, description: str, handler: Callable[..., Any], *, read_only: bool, confirmation: bool = False,
          agents: frozenset[str] = ALL_AGENTS) -> ToolDefinition:
    return ToolDefinition(name, description, handler, read_only, confirmation, agents)


TOOL_REGISTRY: dict[str, ToolDefinition] = {
    "customer_lookup": _tool("customer_lookup", "Retrieve a customer's support account details.", customer_lookup_tool, read_only=True, agents=frozenset({"customer_agent", "sales_agent"})),
    "customer_search": _tool("customer_search", "Search customers by name, email, or company.", customer_search_tool, read_only=True, agents=frozenset({"customer_agent"})),
    "get_ticket": _tool("get_ticket", "Retrieve a support ticket.", get_ticket_tool, read_only=True, agents=frozenset({"technical_agent"})),
    "search_tickets": _tool("search_tickets", "Search support tickets.", search_tickets_tool, read_only=True, agents=frozenset({"technical_agent"})),
    "create_ticket": _tool("create_ticket", "Create a support ticket.", create_ticket_tool, read_only=False, confirmation=True, agents=frozenset({"technical_support_agent", "customer_support_agent"})),
    "update_ticket": _tool("update_ticket", "Update a support ticket.", update_ticket_tool, read_only=False, confirmation=True, agents=frozenset({"technical_support_agent", "customer_support_agent"})),
    "get_invoice": _tool("get_invoice", "Retrieve an invoice or billing record.", get_invoice_tool, read_only=True, agents=frozenset({"billing_agent", "customer_support_agent"})),
    "search_invoices": _tool("search_invoices", "Search billing records.", search_invoices_tool, read_only=True, agents=frozenset({"billing_agent", "customer_support_agent"})),
    "get_payment_status": _tool("get_payment_status", "Retrieve an invoice payment status.", get_payment_status_tool, read_only=True, agents=frozenset({"billing_agent", "customer_support_agent"})),
    "get_refund_status": _tool("get_refund_status", "Retrieve a refund status.", get_refund_status_tool, read_only=True, agents=frozenset({"billing_agent", "customer_support_agent"})),
    "get_customer_crm_profile": _tool("get_customer_crm_profile", "Retrieve account context and recent conversations.", get_customer_crm_profile_tool, read_only=True, agents=frozenset({"sales_agent"})),
    "get_product": _tool("get_product", "Retrieve product details and version.", get_product_tool, read_only=True, agents=frozenset({"product_agent", "sales_agent"})),
    "list_products": _tool("list_products", "List supported products.", list_products_tool, read_only=True, agents=frozenset({"product_agent", "sales_agent"})),
    "search_known_issues": _tool("search_known_issues", "Search documented issues and workarounds.", search_known_issues_tool, read_only=True, agents=frozenset({"technical_agent"})),
    "find_employee": _tool("find_employee", "Retrieve an employee directory record.", find_employee_tool, read_only=True, agents=frozenset({"escalation_agent"})),
    "find_employee_by_skill": _tool("find_employee_by_skill", "Find employees by role or specialization.", find_employee_by_skill_tool, read_only=True, agents=frozenset({"escalation_agent"})),
    "find_support_agent": _tool("find_support_agent", "Find an active human support specialist.", find_support_agent_tool, read_only=True, agents=frozenset({"escalation_agent"})),
    "assign_ticket": _tool("assign_ticket", "Assign a ticket to a human employee.", assign_ticket_tool, read_only=False, confirmation=True, agents=frozenset({"escalation_agent"})),
    "escalate_ticket": _tool("escalate_ticket", "Escalate a ticket for human support.", escalate_ticket_tool, read_only=False, confirmation=True, agents=frozenset({"escalation_agent"})),
    "knowledge_base_search": _tool("knowledge_base_search", "Search the enterprise knowledge base.", knowledge_base_search_tool, read_only=True, agents=frozenset({"billing_agent", "technical_agent", "product_agent", "sales_agent"})),
}


def get_tools_for_agent(agent_name: str) -> list[ToolDefinition]:
    """Return only the tools an agent is allowed to call."""
    return [tool for tool in TOOL_REGISTRY.values() if agent_name in tool.allowed_agents]


def get_tool(name: str, agent_name: str | None = None) -> ToolDefinition:
    """Resolve one tool and, when supplied, enforce the agent allow-list."""
    try:
        tool = TOOL_REGISTRY[name]
    except KeyError as exc:
        raise KeyError(f"Unknown tool: {name}") from exc
    if agent_name is not None and agent_name not in tool.allowed_agents:
        raise ToolPermissionDeniedError(f"Agent '{agent_name}' cannot invoke tool '{name}'.")
    return tool


def invoke_tool(
    name: str,
    agent_name: str,
    *args: Any,
    confirmed: bool = False,
    **kwargs: Any,
) -> Any:
    """Invoke a registered tool with authorization, confirmation, and safe observability."""
    tool = get_tool(name, agent_name)
    if tool.requires_confirmation and not confirmed:
        raise ToolPermissionDeniedError(f"Tool '{name}' requires explicit confirmation.")

    started = perf_counter()
    try:
        result = tool.handler(*args, **kwargs)
    except ToolError:
        logger.info("Tool returned an expected error: name=%s agent=%s duration_ms=%.2f", name, agent_name, (perf_counter() - started) * 1_000)
        raise
    except Exception as exc:
        logger.exception("Tool failed: name=%s agent=%s duration_ms=%.2f", name, agent_name, (perf_counter() - started) * 1_000)
        raise ToolOperationError(f"Tool '{name}' could not complete.") from exc

    logger.info("Tool succeeded: name=%s agent=%s duration_ms=%.2f", name, agent_name, (perf_counter() - started) * 1_000)
    return result
