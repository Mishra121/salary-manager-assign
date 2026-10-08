"""Tests for domain models and business logic."""

import pytest
from decimal import Decimal
from datetime import date

from app.domain.employee import (
    Employee,
    EmploymentType,
    EmployeeStatus,
)
from app.domain.currency import CurrencyConverter, EXCHANGE_RATES


class TestEmployeeModel:
    """Test Employee domain model."""

    def test_create_employee_with_valid_data(self):
        """Employee should be created with valid data."""
        emp = Employee(
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
        )

        assert emp.name == "Alice Johnson"
        assert emp.email == "alice@example.com"
        assert emp.salary == Decimal("120000.00")
        assert emp.employment_type == EmploymentType.FULL_TIME
        assert emp.status == EmployeeStatus.ACTIVE

    def test_employee_salary_must_be_positive(self):
        """Employee salary must be greater than zero."""
        with pytest.raises(ValueError, match="Salary must be positive"):
            Employee(
                name="Bob",
                email="bob@example.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2020, 1, 1),
                salary=Decimal("-50000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_employee_salary_zero_is_invalid(self):
        """Employee salary of zero is invalid."""
        with pytest.raises(ValueError, match="Salary must be positive"):
            Employee(
                name="Charlie",
                email="charlie@example.com",
                job_title="Intern",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.INTERN,
                hire_date=date(2024, 1, 1),
                salary=Decimal("0.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_employee_email_must_be_valid(self):
        """Employee email must be a valid email format."""
        with pytest.raises(ValueError, match="Invalid email"):
            Employee(
                name="David",
                email="not-an-email",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2020, 1, 1),
                salary=Decimal("100000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_employee_name_required(self):
        """Employee name is required and must not be empty."""
        with pytest.raises(ValueError, match="Name is required"):
            Employee(
                name="",
                email="test@example.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                employment_type=EmploymentType.FULL_TIME,
                hire_date=date(2020, 1, 1),
                salary=Decimal("100000.00"),
                currency="USD",
                status=EmployeeStatus.ACTIVE,
            )

    def test_employee_supports_multiple_currencies(self):
        """Employee can have salary in any supported currency."""
        emp_inr = Employee(
            name="Priya Sharma",
            email="priya@example.com",
            job_title="Engineer",
            department="Engineering",
            country="IN",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2021, 6, 1),
            salary=Decimal("1500000.00"),  # INR
            currency="INR",
            status=EmployeeStatus.ACTIVE,
        )

        emp_eur = Employee(
            name="Klaus Mueller",
            email="klaus@example.com",
            job_title="Manager",
            department="Management",
            country="DE",
            employment_type=EmploymentType.FULL_TIME,
            hire_date=date(2019, 3, 1),
            salary=Decimal("85000.00"),  # EUR
            currency="EUR",
            status=EmployeeStatus.ACTIVE,
        )

        assert emp_inr.currency == "INR"
        assert emp_eur.currency == "EUR"


class TestCurrencyConverter:
    """Test currency conversion utilities."""

    def test_convert_usd_to_usd(self):
        """Converting USD to USD should return same amount."""
        amount = Decimal("100.00")
        result = CurrencyConverter.convert(amount, "USD", "USD")
        assert result == Decimal("100.00")

    def test_convert_inr_to_usd(self):
        """Convert INR salary to USD using exchange rate."""
        inr_amount = Decimal("1000000.00")
        usd_amount = CurrencyConverter.convert(inr_amount, "INR", "USD")

        # INR rate is approximately 0.012 (1 INR = 0.012 USD)
        expected = inr_amount * EXCHANGE_RATES["INR"]
        assert usd_amount == expected

    def test_convert_eur_to_usd(self):
        """Convert EUR salary to USD using exchange rate."""
        eur_amount = Decimal("80000.00")
        usd_amount = CurrencyConverter.convert(eur_amount, "EUR", "USD")

        expected = eur_amount * EXCHANGE_RATES["EUR"]
        assert usd_amount == expected

    def test_convert_gbp_to_usd(self):
        """Convert GBP salary to USD using exchange rate."""
        gbp_amount = Decimal("75000.00")
        usd_amount = CurrencyConverter.convert(gbp_amount, "GBP", "USD")

        expected = gbp_amount * EXCHANGE_RATES["GBP"]
        assert usd_amount == expected

    def test_exchange_rates_are_documented(self):
        """Exchange rates should include major currencies."""
        required_currencies = {"USD", "EUR", "GBP", "INR", "AUD", "CAD", "JPY", "SEK", "CHF"}
        assert set(EXCHANGE_RATES.keys()) == required_currencies

    def test_exchange_rate_for_usd_is_one(self):
        """USD should have an exchange rate of 1.0 (base currency)."""
        assert EXCHANGE_RATES["USD"] == Decimal("1.00")

    def test_all_exchange_rates_are_positive(self):
        """All exchange rates must be positive."""
        for currency, rate in EXCHANGE_RATES.items():
            assert rate > 0, f"Exchange rate for {currency} is not positive"
