"""Read-only lookup of documented product issues and workarounds."""

from sqlalchemy.orm import Session

from app.services.known_issue_service import search_known_issues
from app.tools.schemas import KnownIssueSearchInput, KnownIssueToolOutput


def search_known_issues_tool(db: Session, tool_input: KnownIssueSearchInput) -> list[KnownIssueToolOutput]:
    """Find matching known issues; resolved issues are excluded unless explicitly requested."""
    issues = search_known_issues(db, tool_input.query, tool_input.product_id,
                                 tool_input.include_resolved, tool_input.limit)
    return [KnownIssueToolOutput(issue_id=issue.id, title=issue.title, description=issue.description,
                                 severity=issue.severity, status=issue.status, workaround=issue.workaround,
                                 product_id=issue.product_id) for issue in issues]
