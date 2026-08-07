"""Employee data-access operations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Employee


def list_employees(db: Session, skip: int, limit: int) -> list[Employee]:
    return list(db.scalars(select(Employee).order_by(Employee.id).offset(skip).limit(limit)))


def get_employee(db: Session, employee_id: int) -> Employee | None:
    return db.get(Employee, employee_id)
