"""Tests for service layer (business logic)."""

import pytest
from datetime import date
from decimal import Decimal

from app.models import EmployeeModel
from app.services.employee_service import EmployeeService
from app.repositories.employee_repository import EmployeeRepository
from app.domain.employee import EmploymentType, EmployeeStatus


@pytest.fixture
def employee_service(db_session):
    """Create EmployeeService with repository."""
    repo = EmployeeRepository(db_session)
    return EmployeeService(repo)


class TestEmployeeService:
    """Test EmployeeService business logic."""

    def test_create_employee_with_valid_data(self, employee_service):
        """Service should create employee with domain validation."""
        employee = employee_service.create_employee(
            name="Alice Johnson",
            email="alice@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2024, 1, 1),
            salary=Decimal("100000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        )

        assert employee.id is not None
        assert employee.name == "Alice Johnson"
        assert employee.email == "alice@example.com"

    def test_create_employee_rejects_invalid_salary(self, employee_service):
        """Service should reject negative salary."""
        with pytest.raises(ValueError, match="Salary must be positive"):
            employee_service.create_employee(
                name="Bob",
                email="bob@example.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2024, 1, 1),
                salary=Decimal("-50000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_create_employee_rejects_invalid_email(self, employee_service):
        """Service should reject invalid email."""
        with pytest.raises(ValueError, match="Invalid email"):
            employee_service.create_employee(
                name="Charlie",
                email="not-an-email",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2024, 1, 1),
                salary=Decimal("100000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_create_employee_rejects_duplicate_email(self, employee_service):
        """Service should reject duplicate email."""
        # Create first employee
        employee_service.create_employee(
            name="Alice",
            email="alice@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2024, 1, 1),
            salary=Decimal("100000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        )

        # Attempt duplicate email
        with pytest.raises(ValueError, match="Email already exists"):
            employee_service.create_employee(
                name="Alice 2",
                email="alice@example.com",  # Duplicate
                job_title="Manager",
                department="Management",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2024, 1, 1),
                salary=Decimal("120000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_get_employee_by_id(self, employee_service):
        """Service should retrieve employee by ID."""
        created = employee_service.create_employee(
            name="Alice",
            email="alice@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2024, 1, 1),
            salary=Decimal("100000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        )

        retrieved = employee_service.get_employee_by_id(created.id)

        assert retrieved is not None
        assert retrieved.email == "alice@example.com"

    def test_get_employee_by_email(self, employee_service):
        """Service should retrieve employee by email."""
        employee_service.create_employee(
            name="Bob",
            email="bob@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2024, 1, 1),
            salary=Decimal("100000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        )

        retrieved = employee_service.get_employee_by_email("bob@example.com")

        assert retrieved is not None
        assert retrieved.name == "Bob"

    def test_list_employees(self, employee_service):
        """Service should list employees with pagination and filters."""
        for i in range(5):
            employee_service.create_employee(
                name=f"Employee {i}",
                email=f"emp{i}@example.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2024, 1, 1),
                salary=Decimal("100000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

        # List all
        all_employees = employee_service.list_employees()
        assert len(all_employees) == 5

        # List with pagination
        page1 = employee_service.list_employees(skip=0, limit=2)
        assert len(page1) == 2

        page2 = employee_service.list_employees(skip=2, limit=2)
        assert len(page2) == 2

    def test_update_employee(self, employee_service):
        """Service should update employee."""
        created = employee_service.create_employee(
            name="Alice",
            email="alice@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2024, 1, 1),
            salary=Decimal("100000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        )

        updated = employee_service.update_employee(
            created.id,
            job_title="Senior Engineer",
            salary=Decimal("120000.00"),
        )

        assert updated.job_title == "Senior Engineer"
        assert updated.salary == Decimal("120000.00")

    def test_delete_employee(self, employee_service):
        """Service should delete employee."""
        created = employee_service.create_employee(
            name="Alice",
            email="alice@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2024, 1, 1),
            salary=Decimal("100000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        )

        success = employee_service.delete_employee(created.id)

        assert success is True
        retrieved = employee_service.get_employee_by_id(created.id)
        assert retrieved is None

    def test_count_employees(self, employee_service):
        """Service should count employees."""
        for i in range(3):
            employee_service.create_employee(
                name=f"Employee {i}",
                email=f"emp{i}@example.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2024, 1, 1),
                salary=Decimal("100000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

        count = employee_service.count_employees()

        assert count == 3
