"""Service layer for Employee business logic."""

from typing import List, Optional
from decimal import Decimal
from datetime import date

from app.domain.employee import Employee, EmploymentType, EmployeeStatus
from app.repositories.employee_repository import EmployeeRepository
from app.models import EmployeeModel


class EmployeeService:
    """Business logic for employee management."""

    def __init__(self, repo: EmployeeRepository):
        """Initialize service with repository."""
        self.repo = repo

    def create_employee(
        self,
        name: str,
        email: str,
        job_title: str,
        department: str,
        country: str,
        employment_type: EmploymentType,
        hire_date: date,
        salary: Decimal,
        currency: str,
        status: EmployeeStatus,
    ) -> EmployeeModel:
        """
        Create a new employee.

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

        Raises:
            ValueError: If validation fails or email already exists
        """
        # Validate using domain model
        domain_employee = Employee(
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

        # Check for duplicate email
        if self.repo.exists_by_email(email):
            raise ValueError("Email already exists")

        # Create in database
        return self.repo.create(
            name=domain_employee.name,
            email=domain_employee.email,
            job_title=domain_employee.job_title,
            department=domain_employee.department,
            country=domain_employee.country,
            employment_type=domain_employee.employment_type,
            hire_date=domain_employee.hire_date,
            salary=domain_employee.salary,
            currency=domain_employee.currency,
            status=domain_employee.status,
        )

    def get_employee_by_id(self, employee_id: int) -> Optional[EmployeeModel]:
        """
        Get employee by ID.

        Args:
            employee_id: Employee ID

        Returns:
            EmployeeModel or None if not found
        """
        return self.repo.get_by_id(employee_id)

    def get_employee_by_email(self, email: str) -> Optional[EmployeeModel]:
        """
        Get employee by email.

        Args:
            email: Employee email

        Returns:
            EmployeeModel or None if not found
        """
        return self.repo.get_by_email(email)

    def list_employees(
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
        List employees with optional filters.

        Args:
            skip: Number of records to skip
            limit: Number of records to return
            search: Search string
            country: Filter by country
            department: Filter by department
            job_title: Filter by job title
            status: Filter by employment status

        Returns:
            List of EmployeeModel objects
        """
        return self.repo.list(
            skip=skip,
            limit=limit,
            search=search,
            country=country,
            department=department,
            job_title=job_title,
            status=status,
        )

    def update_employee(
        self, employee_id: int, **kwargs
    ) -> Optional[EmployeeModel]:
        """
        Update employee.

        Args:
            employee_id: Employee ID
            **kwargs: Fields to update

        Returns:
            Updated EmployeeModel or None if not found
        """
        return self.repo.update(employee_id, **kwargs)

    def delete_employee(self, employee_id: int) -> bool:
        """
        Delete employee.

        Args:
            employee_id: Employee ID

        Returns:
            True if deleted, False if not found
        """
        return self.repo.delete(employee_id)

    def count_employees(
        self,
        country: Optional[str] = None,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
        status: Optional[EmployeeStatus] = None,
    ) -> int:
        """
        Count employees.

        Args:
            country: Filter by country
            department: Filter by department
            job_title: Filter by job title
            status: Filter by employment status

        Returns:
            Number of matching employees
        """
        return self.repo.count(
            country=country,
            department=department,
            job_title=job_title,
            status=status,
        )
