"""Tests for salary history tracking."""

import pytest
from datetime import date
from decimal import Decimal

from app.models import EmployeeModel, SalaryHistoryModel
from app.repositories.salary_history_repository import SalaryHistoryRepository
from app.services.salary_history_service import SalaryHistoryService
from app.domain.employee import EmploymentType, EmployeeStatus


class TestSalaryHistoryRepository:
    """Test SalaryHistoryRepository data access."""

    def test_create_salary_history_record(self, db_session):
        """Repository should create immutable salary history record."""
        # Create employee first
        emp = EmployeeModel(
            name="Alice",
            email="alice@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=Decimal("100000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)

        # Record first salary (initial hire)
        history = repo.create(
            employee_id=emp.id,
            old_salary=None,
            new_salary=Decimal("100000"),
            currency="USD",
            effective_date=date(2023, 1, 1),
            reason="Initial hire",
        )

        assert history.id is not None
        assert history.employee_id == emp.id
        assert history.old_salary is None
        assert history.new_salary == Decimal("100000")
        assert history.reason == "Initial hire"

    def test_create_salary_change_record(self, db_session):
        """Repository should record salary changes with old/new values."""
        emp = EmployeeModel(
            name="Bob",
            email="bob@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=Decimal("120000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)

        history = repo.create(
            employee_id=emp.id,
            old_salary=Decimal("100000"),
            new_salary=Decimal("120000"),
            currency="USD",
            effective_date=date(2024, 1, 1),
            reason="Annual raise",
        )

        assert history.old_salary == Decimal("100000")
        assert history.new_salary == Decimal("120000")
        assert history.reason == "Annual raise"

    def test_get_history_for_employee(self, db_session):
        """Repository should retrieve complete salary history for employee."""
        emp = EmployeeModel(
            name="Charlie",
            email="charlie@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2022, 1, 1),
            salary=Decimal("130000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)

        # Add multiple history records
        repo.create(emp.id, None, Decimal("100000"), "USD", date(2022, 1, 1), "Initial hire")
        repo.create(emp.id, Decimal("100000"), Decimal("110000"), "USD", date(2023, 1, 1), "Annual raise")
        repo.create(emp.id, Decimal("110000"), Decimal("130000"), "USD", date(2024, 1, 1), "Promotion")

        history = repo.get_by_employee_id(emp.id)

        assert len(history) == 3
        # Should be ordered by effective_date ascending
        assert history[0].new_salary == Decimal("100000")
        assert history[1].new_salary == Decimal("110000")
        assert history[2].new_salary == Decimal("130000")

    def test_get_history_returns_empty_for_no_records(self, db_session):
        """Repository should return empty list if no history exists."""
        repo = SalaryHistoryRepository(db_session)

        history = repo.get_by_employee_id(999)  # Non-existent employee

        assert history == []

    def test_history_ordered_by_effective_date(self, db_session):
        """Repository should return history in chronological order."""
        emp = EmployeeModel(
            name="Diana",
            email="diana@acme.com",
            job_title="Manager",
            department="Management",
            country="US",
            hire_date=date(2021, 1, 1),
            salary=Decimal("150000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)

        # Add records out of order
        repo.create(emp.id, Decimal("120000"), Decimal("150000"), "USD", date(2024, 1, 1), "Promotion")
        repo.create(emp.id, None, Decimal("100000"), "USD", date(2021, 1, 1), "Initial hire")
        repo.create(emp.id, Decimal("100000"), Decimal("120000"), "USD", date(2023, 1, 1), "Raise")

        history = repo.get_by_employee_id(emp.id)

        # Should be sorted by effective_date
        dates = [h.effective_date for h in history]
        assert dates == sorted(dates)
        assert dates == [date(2021, 1, 1), date(2023, 1, 1), date(2024, 1, 1)]


class TestSalaryHistoryService:
    """Test SalaryHistoryService business logic."""

    def test_record_initial_hire_salary(self, db_session):
        """Service should record initial salary on hire."""
        emp = EmployeeModel(
            name="Eve",
            email="eve@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=Decimal("100000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        service = SalaryHistoryService(SalaryHistoryRepository(db_session))

        service.record_salary_change(
            employee_id=emp.id,
            old_salary=None,
            new_salary=Decimal("100000"),
            currency="USD",
            effective_date=date(2023, 1, 1),
            reason="Initial hire",
        )

        repo = SalaryHistoryRepository(db_session)
        history = repo.get_by_employee_id(emp.id)

        assert len(history) == 1
        assert history[0].reason == "Initial hire"

    def test_record_salary_raise(self, db_session):
        """Service should record salary changes with reasons."""
        emp = EmployeeModel(
            name="Frank",
            email="frank@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2022, 1, 1),
            salary=Decimal("110000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        service = SalaryHistoryService(SalaryHistoryRepository(db_session))

        service.record_salary_change(
            employee_id=emp.id,
            old_salary=Decimal("100000"),
            new_salary=Decimal("110000"),
            currency="USD",
            effective_date=date(2023, 1, 1),
            reason="Annual raise - 10% merit increase",
        )

        repo = SalaryHistoryRepository(db_session)
        history = repo.get_by_employee_id(emp.id)

        assert len(history) == 1
        assert history[0].reason == "Annual raise - 10% merit increase"
        assert history[0].old_salary == Decimal("100000")

    def test_get_current_salary_from_latest_history(self, db_session):
        """Service should determine current salary from most recent history."""
        emp = EmployeeModel(
            name="Grace",
            email="grace@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2021, 1, 1),
            salary=Decimal("130000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)
        repo.create(emp.id, None, Decimal("100000"), "USD", date(2021, 1, 1), "Initial")
        repo.create(emp.id, Decimal("100000"), Decimal("120000"), "USD", date(2022, 1, 1), "Raise")
        repo.create(emp.id, Decimal("120000"), Decimal("130000"), "USD", date(2023, 1, 1), "Promotion")

        service = SalaryHistoryService(repo)
        current = service.get_current_salary(emp.id)

        assert current == Decimal("130000")

    def test_get_total_raise_over_period(self, db_session):
        """Service should calculate total raise from initial to current."""
        emp = EmployeeModel(
            name="Henry",
            email="henry@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2020, 1, 1),
            salary=Decimal("150000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)
        repo.create(emp.id, None, Decimal("100000"), "USD", date(2020, 1, 1), "Initial")
        repo.create(emp.id, Decimal("100000"), Decimal("120000"), "USD", date(2021, 1, 1), "Raise")
        repo.create(emp.id, Decimal("120000"), Decimal("150000"), "USD", date(2022, 1, 1), "Promotion")

        service = SalaryHistoryService(repo)
        total_raise = service.get_total_raise(emp.id)

        # (150000 - 100000) / 100000 * 100 = 50%
        assert total_raise == 50.0

    def test_get_salary_timeline(self, db_session):
        """Service should return formatted salary timeline."""
        emp = EmployeeModel(
            name="Iris",
            email="iris@acme.com",
            job_title="Manager",
            department="Management",
            country="US",
            hire_date=date(2020, 1, 1),
            salary=Decimal("140000"),
            currency="USD",
        )
        db_session.add(emp)
        db_session.commit()

        repo = SalaryHistoryRepository(db_session)
        repo.create(emp.id, None, Decimal("100000"), "USD", date(2020, 1, 1), "Initial")
        repo.create(emp.id, Decimal("100000"), Decimal("120000"), "USD", date(2021, 1, 1), "Raise")
        repo.create(emp.id, Decimal("120000"), Decimal("140000"), "USD", date(2023, 1, 1), "Promotion")

        service = SalaryHistoryService(repo)
        timeline = service.get_salary_timeline(emp.id)

        assert len(timeline) == 3
        assert timeline[0]["new_salary"] == Decimal("100000")
        assert timeline[1]["new_salary"] == Decimal("120000")
        assert timeline[2]["new_salary"] == Decimal("140000")
        assert all("effective_date" in t for t in timeline)
        assert all("reason" in t for t in timeline)
