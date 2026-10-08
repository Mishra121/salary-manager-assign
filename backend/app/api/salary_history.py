"""API routes for salary history."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    SalaryHistoryResponse,
    RecordSalaryChangeRequest,
    SalaryHistoryRecord,
)
from app.repositories.salary_history_repository import SalaryHistoryRepository
from app.services.salary_history_service import SalaryHistoryService
from app.repositories.employee_repository import EmployeeRepository

router = APIRouter(prefix="/employees", tags=["salary-history"])


def get_salary_history_service(db: Session = Depends(get_db)) -> SalaryHistoryService:
    """Dependency to get SalaryHistoryService."""
    repo = SalaryHistoryRepository(db)
    return SalaryHistoryService(repo)


@router.get("/{employee_id}/salary-history", response_model=SalaryHistoryResponse)
def get_employee_salary_history(
    employee_id: int,
    db: Session = Depends(get_db),
    service: SalaryHistoryService = Depends(get_salary_history_service),
):
    """
    Get complete salary history for an employee.

    Returns timeline of all salary changes with full record data (old_salary, new_salary, reason),
    effective dates, calculated change percentages, and summary analytics.
    """
    emp_repo = EmployeeRepository(db)
    employee = emp_repo.get_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    timeline = service.get_salary_timeline(employee_id)
    current_salary = service.get_current_salary(employee_id)
    total_raise = service.get_total_raise(employee_id)
    count = service.get_salary_history_count(employee_id)

    return SalaryHistoryResponse(
        employee_id=employee_id,
        current_salary=current_salary or 0,
        total_raise_percentage=total_raise,
        history_count=count,
        timeline=[
            {
                "id": t["id"],
                "employee_id": t["employee_id"],
                "old_salary": t.get("old_salary"),
                "new_salary": t["new_salary"],
                "currency": t["currency"],
                "effective_date": t["effective_date"],
                "reason": t["reason"],
                "change_percentage": t.get("change_percentage"),
            }
            for t in timeline
        ],
    )


@router.post("/{employee_id}/salary-history", response_model=SalaryHistoryRecord, status_code=status.HTTP_201_CREATED)
def record_salary_change(
    employee_id: int,
    request: RecordSalaryChangeRequest,
    db: Session = Depends(get_db),
    service: SalaryHistoryService = Depends(get_salary_history_service),
):
    """
    Record a salary change for an employee.

    Creates an immutable history record with the old and new salary, effective date, and reason.
    """
    emp_repo = EmployeeRepository(db)
    employee = emp_repo.get_by_id(employee_id)
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    try:
        result = service.record_salary_change(
            employee_id=employee_id,
            old_salary=request.old_salary,
            new_salary=request.new_salary,
            currency=request.currency,
            effective_date=request.effective_date,
            reason=request.reason,
        )

        return SalaryHistoryRecord(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
