"""Employee REST endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.api import EmployeeRead
from app.schemas.response import APIResponse
from app.services import employee_service

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", response_model=APIResponse[list[EmployeeRead]])
def list_employees(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=500), db: Session = Depends(get_db)) -> APIResponse[list[EmployeeRead]]:
    employees = employee_service.list_employees(db, skip, limit)
    return APIResponse(success=True, message="Employees retrieved successfully.", data=[EmployeeRead.model_validate(employee) for employee in employees])


@router.get("/{employee_id}", response_model=APIResponse[EmployeeRead])
def get_employee(employee_id: int, db: Session = Depends(get_db)) -> APIResponse[EmployeeRead]:
    employee = employee_service.get_employee(db, employee_id)
    if employee is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Employee not found.")
    return APIResponse(success=True, message="Employee retrieved successfully.", data=EmployeeRead.model_validate(employee))
