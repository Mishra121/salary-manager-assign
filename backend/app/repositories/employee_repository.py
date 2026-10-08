"""Repository for Employee data access."""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import EmployeeModel
from app.domain.employee import EmploymentType, EmployeeStatus


class EmployeeRepository:
    """Data access layer for Employee entity."""

    def __init__(self, db: Session):
        """Initialize repository with database session."""
        self.db = db

    def create(
        self,
        name: str,
        email: str,
        job_title: str,
        department: str,
        country: str,
        employment_type: EmploymentType,
        hire_date,
        salary,
        currency: str,
        status: EmployeeStatus,
    ) -> EmployeeModel:
        """
        Create and persist a new employee.

        Args:
            name: Employee name
            email: Employee email
            job_title: Job title
            department: Department
            country: Country code
            employment_type: Type of employment
            hire_date: Hire date
            salary: Salary amount
            currency: Currency code
            status: Employment status

        Returns:
            Created EmployeeModel
        """
        employee = EmployeeModel(
            name=name,
            email=email,
            job_title=job_title,
            department=department,
            country=country,
            employment_type=employment_type,
            hire_date=hire_date,
            salary=salary,
            currency=currency,
            status=status,
        )

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)

        return employee

    def get_by_id(self, employee_id: int) -> Optional[EmployeeModel]:
        """
        Retrieve employee by ID.

        Args:
            employee_id: Employee ID

        Returns:
            EmployeeModel or None if not found
        """
        return self.db.query(EmployeeModel).filter(EmployeeModel.id == employee_id).first()

    def get_by_email(self, email: str) -> Optional[EmployeeModel]:
        """
        Retrieve employee by email.

        Args:
            email: Employee email

        Returns:
            EmployeeModel or None if not found
        """
        return self.db.query(EmployeeModel).filter(
            EmployeeModel.email == email.lower()
        ).first()

    def list(
        self,
        skip: int = 0,
        limit: int = 50,
        search: Optional[str] = None,
        country: Optional[str] = None,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
    ) -> List[EmployeeModel]:
        """
        List employees with optional filters and pagination.

        Args:
            skip: Number of records to skip (for pagination)
            limit: Number of records to return (default 50, max recommended 200)
            search: Search string (searches name and email)
            country: Filter by country
            department: Filter by department
            job_title: Filter by job title
            status: Filter by employment status

        Returns:
            List of EmployeeModel objects
        """
        query = self.db.query(EmployeeModel)

        # Apply search filter (name or email)
        if search:
            search_term = f"%{search.lower()}%"
            query = query.filter(
                (func.lower(EmployeeModel.name).like(search_term))
                | (func.lower(EmployeeModel.email).like(search_term))
            )

        # Apply exact filters
        if country:
            query = query.filter(EmployeeModel.country == country)

        if department:
            query = query.filter(EmployeeModel.department == department)

        if job_title:
            query = query.filter(EmployeeModel.job_title == job_title)

        if status:
            query = query.filter(EmployeeModel.status == status)

        # Apply pagination
        return query.offset(skip).limit(limit).all()

    def update(self, employee_id: int, **kwargs) -> Optional[EmployeeModel]:
        """
        Update employee fields.

        Args:
            employee_id: Employee ID
            **kwargs: Fields to update (name, email, job_title, etc.)

        Returns:
            Updated EmployeeModel or None if not found
        """
        employee = self.get_by_id(employee_id)
        if not employee:
            return None

        # Only update allowed fields
        allowed_fields = {
            "name",
            "email",
            "job_title",
            "department",
            "country",
            "employment_type",
            "hire_date",
            "salary",
            "currency",
            "status",
        }

        for field, value in kwargs.items():
            if field in allowed_fields and value is not None:
                setattr(employee, field, value)

        self.db.commit()
        self.db.refresh(employee)

        return employee

    def delete(self, employee_id: int) -> bool:
        """
        Delete employee by ID.

        Args:
            employee_id: Employee ID

        Returns:
            True if deleted, False if not found
        """
        employee = self.get_by_id(employee_id)
        if not employee:
            return False

        self.db.delete(employee)
        self.db.commit()

        return True

    def count(
        self,
        country: Optional[str] = None,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
    ) -> int:
        """
        Count employees with optional filters.

        Args:
            country: Filter by country
            department: Filter by department
            job_title: Filter by job title
            status: Filter by employment status

        Returns:
            Number of matching employees
        """
        query = self.db.query(EmployeeModel)

        if country:
            query = query.filter(EmployeeModel.country == country)

        if department:
            query = query.filter(EmployeeModel.department == department)

        if job_title:
            query = query.filter(EmployeeModel.job_title == job_title)

        if status:
            query = query.filter(EmployeeModel.status == status)

        return query.count()

    def exists_by_email(self, email: str) -> bool:
        """
        Check if employee with email exists.

        Args:
            email: Employee email

        Returns:
            True if exists, False otherwise
        """
        return (
            self.db.query(EmployeeModel)
            .filter(EmployeeModel.email == email.lower())
            .first()
            is not None
        )
