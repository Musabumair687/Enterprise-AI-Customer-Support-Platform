"""Known-issue data-access operations."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.models import KnownIssue


def search_known_issues(
    db: Session,
    query: str,
    product_id: int | None,
    include_resolved: bool,
    limit: int,
) -> list[KnownIssue]:
    """Search documented issues and their workarounds without exposing ORM details to tools."""
    pattern = f"%{query.strip()}%"
    statement = select(KnownIssue).where(
        or_(KnownIssue.title.ilike(pattern), KnownIssue.description.ilike(pattern))
    )
    if product_id is not None:
        statement = statement.where(KnownIssue.product_id == product_id)
    if not include_resolved:
        statement = statement.where(KnownIssue.status != "resolved")
    return list(db.scalars(statement.order_by(KnownIssue.updated_at.desc()).limit(limit)))
