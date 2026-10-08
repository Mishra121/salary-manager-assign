"""Tests for repository layer (data access)."""

import pytest
from datetime import date
from decimal import Decimal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, EmployeeModel, SalaryHistoryModel
from app.repositories.employee_repository import EmployeeRepository
from app.domain.employee import EmploymentType, EmployeeStatus


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_employees(db_session):
    """Create sample employees for testing."""
    employees = [
        EmployeeModel(
            name="Alice Johnson",
            email="alice@example.com",
            job_title="Senior Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2020, 1, 15),
            salary=Decimal("120000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        ),
        EmployeeModel(
            name="Bob Smith",
            email="bob@example.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2021, 6, 1),
            salary=Decimal("95000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        ),
        EmployeeModel(
            name="Priya Sharma",
            email="priya@example.com",
            job_title="Engineer",
            department="Engineering",
            country="IN",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2021, 3, 15),
            salary=Decimal("1500000.00"),
            currency="INR",
            status=EmployeeStatus.ACTIVE,
        ),
        EmployeeModel(
            name="Charlie Brown",
            email="charlie@example.com",
            job_title="Manager",
            department="Management",
            country="US",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2019, 1, 1),
            salary=Decimal("150000.00"),
            currency="USD",
            status=EmployeeStatus.ACTIVE,
        ),
    ]

    for emp in employees:
        db_session.add(emp)

    db_session.commit()

    return employees


class TestEmployeeRepository:
    """Test EmployeeRepository CRUD operations."""

    def test_create_employee(self, db_session):
        """Repository should create and persist employee."""
        repo = EmployeeRepository(db_session)

        emp_data = {
            "name": "Test User",
            "email": "test@example.com",
            "job_title": "Engineer",
            "department": "Engineering",
            "country": "US",
            "employment_type": EmploymentType.FULL_TIME,
            "hire_date": date(2024, 1, 1),
            "salary": Decimal("100000.00"),
            "currency": "USD",
            "status": EmployeeStatus.ACTIVE,
        }

        employee = repo.create(**emp_data)

        assert employee.id is not None
        assert employee.name == "Test User"
        assert employee.email == "test@example.com"

    def test_get_employee_by_id(self, db_session, sample_employees):
        """Repository should retrieve employee by ID."""
        repo = EmployeeRepository(db_session)
        emp_id = sample_employees[0].id

        employee = repo.get_by_id(emp_id)

        assert employee is not None
        assert employee.email == "alice@example.com"

    def test_get_employee_by_email(self, db_session, sample_employees):
        """Repository should retrieve employee by email."""
        repo = EmployeeRepository(db_session)

        employee = repo.get_by_email("bob@example.com")

        assert employee is not None
        assert employee.name == "Bob Smith"

    def test_get_employee_by_email_returns_none_if_not_found(self, db_session):
        """Repository should return None if email not found."""
        repo = EmployeeRepository(db_session)

        employee = repo.get_by_email("nonexistent@example.com")

        assert employee is None

    def test_list_all_employees(self, db_session, sample_employees):
        """Repository should list all employees."""
        repo = EmployeeRepository(db_session)

        employees = repo.list()

        assert len(employees) == 4

    def test_list_with_pagination(self, db_session, sample_employees):
        """Repository should support pagination."""
        repo = EmployeeRepository(db_session)

        # Get first 2 employees
        page1 = repo.list(skip=0, limit=2)
        assert len(page1) == 2

        # Get next 2 employees
        page2 = repo.list(skip=2, limit=2)
        assert len(page2) == 2

        # Get beyond available
        page3 = repo.list(skip=4, limit=2)
        assert len(page3) == 0

    def test_list_with_filter_by_country(self, db_session, sample_employees):
        """Repository should filter employees by country."""
        repo = EmployeeRepository(db_session)

        us_employees = repo.list(country="US")

        assert len(us_employees) == 3
        assert all(emp.country == "US" for emp in us_employees)

    def test_list_with_filter_by_department(self, db_session, sample_employees):
        """Repository should filter employees by department."""
        repo = EmployeeRepository(db_session)

        eng_employees = repo.list(department="Engineering")

        assert len(eng_employees) == 3
        assert all(emp.department == "Engineering" for emp in eng_employees)

    def test_list_with_filter_by_job_title(self, db_session, sample_employees):
        """Repository should filter employees by job title."""
        repo = EmployeeRepository(db_session)

        engineers = repo.list(job_title="Engineer")

        assert len(engineers) == 2
        assert all(emp.job_title == "Engineer" for emp in engineers)

    def test_list_with_search_by_name(self, db_session, sample_employees):
        """Repository should search by name (substring match)."""
        repo = EmployeeRepository(db_session)

        results = repo.list(search="priya")

        assert len(results) == 1
        assert results[0].email == "priya@example.com"

    def test_list_with_search_by_email(self, db_session, sample_employees):
        """Repository should search by email (substring match)."""
        repo = EmployeeRepository(db_session)

        results = repo.list(search="example.com")

        assert len(results) == 4

    def test_list_with_combined_filters(self, db_session, sample_employees):
        """Repository should support combined filters."""
        repo = EmployeeRepository(db_session)

        results = repo.list(country="US", department="Engineering")

        assert len(results) == 2

    def test_update_employee(self, db_session, sample_employees):
        """Repository should update employee."""
        repo = EmployeeRepository(db_session)
        emp_id = sample_employees[0].id

        updated = repo.update(emp_id, job_title="Principal Engineer")

        assert updated.job_title == "Principal Engineer"

    def test_delete_employee(self, db_session, sample_employees):
        """Repository should delete employee."""
        repo = EmployeeRepository(db_session)
        emp_id = sample_employees[0].id

        success = repo.delete(emp_id)

        assert success is True
        deleted = repo.get_by_id(emp_id)
        assert deleted is None

    def test_count_employees(self, db_session, sample_employees):
        """Repository should count total employees."""
        repo = EmployeeRepository(db_session)

        count = repo.count()

        assert count == 4

    def test_count_with_filter(self, db_session, sample_employees):
        """Repository should count with filters."""
        repo = EmployeeRepository(db_session)

        us_count = repo.count(country="US")

        assert us_count == 3

    def test_exists_by_email(self, db_session, sample_employees):
        """Repository should check if email exists."""
        repo = EmployeeRepository(db_session)

        assert repo.exists_by_email("alice@example.com") is True
        assert repo.exists_by_email("nonexistent@example.com") is False
