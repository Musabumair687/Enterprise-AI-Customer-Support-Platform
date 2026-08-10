"""Read-only employee directory tools for human-support routing."""

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.models import Employee
from app.services.employee_service import get_employee
from app.tools.errors import ToolNotFoundError
from app.tools.schemas import EmployeeLookupInput, EmployeeSearchInput, EmployeeToolOutput


def _employee_output(employee: Employee) -> EmployeeToolOutput:
    return EmployeeToolOutput(employee_id=employee.id, name=employee.name, email=employee.email,
                              role=employee.role, is_active=employee.is_active)


def find_employee_tool(db: Session, tool_input: EmployeeLookupInput) -> EmployeeToolOutput:
    """Retrieve one employee who may receive an escalated support case."""
    employee = get_employee(db, tool_input.employee_id)
    if employee is None:
        raise ToolNotFoundError(f"Employee {tool_input.employee_id} was not found.")
    return _employee_output(employee)


def find_employee_by_skill_tool(db: Session, tool_input: EmployeeSearchInput) -> list[EmployeeToolOutput]:
    """Search employee names and role labels; roles are the available skill taxonomy today."""
    pattern = f"%{tool_input.query.strip()}%"
    statement = select(Employee).where(or_(Employee.name.ilike(pattern), Employee.role.ilike(pattern)))
    if tool_input.active_only:
        statement = statement.where(Employee.is_active.is_(True))
    return [_employee_output(employee) for employee in db.scalars(statement.order_by(Employee.name).limit(tool_input.limit))]


def find_support_agent_tool(db: Session, tool_input: EmployeeSearchInput) -> list[EmployeeToolOutput]:
    """Find active support-role employees matching a requested specialization or name."""
    pattern = f"%{tool_input.query.strip()}%"
    statement = select(Employee).where(
        Employee.is_active.is_(True),
        Employee.role.ilike("%support%"),
        or_(Employee.name.ilike(pattern), Employee.role.ilike(pattern)),
    )
    return [
        _employee_output(employee)
        for employee in db.scalars(statement.order_by(Employee.name).limit(tool_input.limit))
    ]
