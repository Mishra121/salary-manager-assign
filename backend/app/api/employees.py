"""API routes for employee management."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate, EmployeeListResponse
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.domain.employee import EmployeeStatus

router = APIRouter(prefix="/employees", tags=["employees"])


def get_service(db: Session = Depends(get_db)) -> EmployeeService:
    """Get employee service with repository."""
    repo = EmployeeRepository(db)
    return EmployeeService(repo)


@router.get("", response_model=EmployeeListResponse)
def list_employees(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, gt=0, le=200, description="Number of records to return"),
    search: str = Query(None, description="Search by name or email"),
    country: str = Query(None, description="Filter by country"),
    department: str = Query(None, description="Filter by department"),
    job_title: str = Query(None, description="Filter by job title"),
    service: EmployeeService = Depends(get_service),
) -> EmployeeListResponse:
    """
    List employees with optional filters and pagination.

    - **skip**: Number of records to skip (default: 0)
    - **limit**: Number of records to return (default: 50, max: 200)
    - **search**: Search by name or email (substring match)
    - **country**: Filter by country code
    - **department**: Filter by department name
    - **job_title**: Filter by job title
    """
    employees = service.list_employees(
        skip=skip,
        limit=limit,
        search=search,
        country=country,
        department=department,
        job_title=job_title,
    )

    total = service.count_employees(
        country=country,
        department=department,
        job_title=job_title,
    )

    return EmployeeListResponse(
        total=total,
        skip=skip,
        limit=limit,
        employees=[EmployeeResponse.model_validate(emp) for emp in employees],
    )


@router.post("", response_model=EmployeeResponse, status_code=201)
def create_employee(
    emp_create: EmployeeCreate,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    """
    Create a new employee.

    - **name**: Employee's full name
    - **email**: Unique email address
    - **job_title**: Job title/position
    - **department**: Department name
    - **country**: Country code (ISO 3166-1 alpha-2)
    - **employment_type**: Type of employment
    - **hire_date**: Date of hire
    - **salary**: Salary amount (must be positive)
    - **currency**: Currency code (ISO 4217, default: USD)
    - **status**: Employment status (default: active)
    """
    try:
        employee = service.create_employee(
            name=emp_create.name,
            email=emp_create.email,
            job_title=emp_create.job_title,
            department=emp_create.department,
            country=emp_create.country,
            employment_type=emp_create.employment_type,
            hire_date=emp_create.hire_date,
            salary=emp_create.salary,
            currency=emp_create.currency,
            status=emp_create.status,
        )
        return EmployeeResponse.model_validate(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    """Get employee by ID."""
    employee = service.get_employee_by_id(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse.model_validate(employee)


@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(
    employee_id: int,
    emp_update: EmployeeUpdate,
    service: EmployeeService = Depends(get_service),
) -> EmployeeResponse:
    """Update employee fields (all fields optional)."""
    # Prepare update data (only non-None values)
    update_data = emp_update.model_dump(exclude_unset=True)

    try:
        employee = service.update_employee(employee_id, **update_data)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return EmployeeResponse.model_validate(employee)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{employee_id}", status_code=204)
def delete_employee(
    employee_id: int,
    service: EmployeeService = Depends(get_service),
) -> None:
    """Delete employee by ID."""
    success = service.delete_employee(employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")
