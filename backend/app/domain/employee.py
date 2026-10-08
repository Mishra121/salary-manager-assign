"""Employee domain model and related enums."""

from enum import Enum
from datetime import date
from decimal import Decimal
import re


class EmploymentType(str, Enum):
    """Employment type enumeration."""
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    CONTRACT = "CONTRACT"
    INTERN = "INTERN"


class EmployeeStatus(str, Enum):
    """Employee status enumeration."""
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    LEAVE = "LEAVE"
    TERMINATED = "TERMINATED"


class Employee:
    """Employee domain model with business logic and validation."""

    def __init__(
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
    ):
        """
        Initialize an Employee.

        Args:
            name: Employee's full name
            email: Employee's email address
            job_title: Job title/position
            department: Department name
            country: Country code (e.g., 'US', 'IN', 'DE')
            employment_type: Type of employment
            hire_date: Date of hire
            salary: Current salary amount
            currency: Currency code (e.g., 'USD', 'INR', 'EUR')
            status: Current employment status

        Raises:
            ValueError: If any validation fails
        """
        # Validate name
        if not name or not name.strip():
            raise ValueError("Name is required")

        # Validate email
        if not self._is_valid_email(email):
            raise ValueError("Invalid email")

        # Validate salary
        if salary <= 0:
            raise ValueError("Salary must be positive")

        self.name = name.strip()
        self.email = email.strip().lower()
        self.job_title = job_title
        self.department = department
        self.country = country
        self.employment_type = employment_type
        self.hire_date = hire_date
        self.salary = salary
        self.currency = currency
        self.status = status

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """
        Validate email format.

        Args:
            email: Email address to validate

        Returns:
            True if email is valid, False otherwise
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None

    def __repr__(self) -> str:
        """String representation of Employee."""
        return (
            f"Employee(name={self.name!r}, email={self.email!r}, "
            f"job_title={self.job_title!r}, salary={self.salary})"
        )

    def __eq__(self, other: object) -> bool:
        """Check equality based on email (unique identifier)."""
        if not isinstance(other, Employee):
            return NotImplemented
        return self.email == other.email
