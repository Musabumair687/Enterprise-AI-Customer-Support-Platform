"""Select an available employee for an escalation using database-backed routing."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Employee


class AssignmentService:
    def assign(self, db: Session, department: str, issue: str) -> Employee | None:
        """Return the first active best-fit employee, with a safe support fallback."""
        terms = {department.casefold(), *issue.casefold().split()}
        employees = list(db.scalars(select(Employee).where(Employee.is_active.is_(True)).order_by(Employee.id)))
        def score(employee: Employee) -> int:
            role = employee.role.casefold()
            return sum(term in role for term in terms)
        return max(employees, key=score, default=None)
