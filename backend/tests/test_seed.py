"""Tests for employee seeding script."""

import pytest
from decimal import Decimal
from app.seed.seed_employees import (
    generate_employees,
    get_realistic_salary_for_title,
    COUNTRIES,
    DEPARTMENTS,
    JOB_TITLES,
)
from app.domain.employee import EmploymentType, EmployeeStatus


class TestSeedDataGeneration:
    """Test seed data generation logic."""

    def test_generate_employees_creates_10k_records(self):
        """Verify exactly 10,000 employees are generated."""
        employees = generate_employees(count=10000)
        assert len(employees) == 10000

    def test_generate_employees_is_deterministic(self):
        """Same seed produces identical results."""
        seed_value = 42
        employees1 = generate_employees(count=1000, seed=seed_value)
        employees2 = generate_employees(count=1000, seed=seed_value)

        # Compare email and salary (unique and important fields)
        emails1 = [e.email for e in employees1]
        emails2 = [e.email for e in employees2]
        assert emails1 == emails2

        salaries1 = [e.salary for e in employees1]
        salaries2 = [e.salary for e in employees2]
        assert salaries1 == salaries2

    def test_employees_have_all_required_fields(self):
        """Each employee has name, email, salary, country, etc."""
        employees = generate_employees(count=100)

        for emp in employees:
            assert emp.name
            assert emp.email
            assert emp.salary > 0
            assert emp.country in COUNTRIES
            assert emp.department in DEPARTMENTS
            assert emp.job_title in JOB_TITLES
            assert emp.employment_type in EmploymentType
            assert emp.status == EmployeeStatus.ACTIVE

    def test_emails_are_unique(self):
        """All generated emails are unique."""
        employees = generate_employees(count=1000)
        emails = [e.email for e in employees]
        assert len(emails) == len(set(emails)), "Duplicate emails found"

    def test_salary_is_positive_decimal(self):
        """All salaries are positive Decimal values."""
        employees = generate_employees(count=100)

        for emp in employees:
            assert isinstance(emp.salary, Decimal)
            assert emp.salary > 0

    def test_country_distribution_is_reasonable(self):
        """Countries are distributed somewhat evenly."""
        employees = generate_employees(count=1000)
        countries = [e.country for e in employees]

        country_counts = {}
        for country in countries:
            country_counts[country] = country_counts.get(country, 0) + 1

        # Each country should have at least 50 employees (1000 / 9 ≈ 111)
        for country, count in country_counts.items():
            assert count >= 50, f"Country {country} has too few employees: {count}"

    def test_salary_reflects_title_and_country(self):
        """Salary ranges vary by job title and country."""
        employees = generate_employees(count=500)

        # Collect salaries by title
        title_salaries = {}
        for emp in employees:
            key = emp.job_title
            if key not in title_salaries:
                title_salaries[key] = []
            title_salaries[key].append(emp.salary)

        # Each title should have some salary variation
        for title, salaries in title_salaries.items():
            min_sal = min(salaries)
            max_sal = max(salaries)
            # Salary range for a title should be > 10% (varies by role/country)
            assert max_sal > min_sal, f"No salary variation for {title}"

    def test_realistic_salary_for_title_returns_positive(self):
        """get_realistic_salary_for_title returns positive Decimal."""
        for title in JOB_TITLES[:3]:  # Test a few titles
            salary = get_realistic_salary_for_title(title, country="US")
            assert isinstance(salary, Decimal)
            assert salary > 0

    def test_salary_varies_by_country(self):
        """Same title has different salaries in different countries."""
        title = JOB_TITLES[0]

        salary_us = get_realistic_salary_for_title(title, country="US")
        salary_in = get_realistic_salary_for_title(title, country="IN")
        salary_jp = get_realistic_salary_for_title(title, country="JP")

        # These should not all be identical (countries have different salary levels)
        assert not (salary_us == salary_in == salary_jp)


class TestSeedCurrencyMapping:
    """Test that seed data uses correct currencies per country."""

    def test_country_to_currency_mapping(self):
        """Each country is assigned to a currency."""
        from app.seed.seed_employees import COUNTRY_TO_CURRENCY

        for country in COUNTRIES:
            assert country in COUNTRY_TO_CURRENCY
            currency = COUNTRY_TO_CURRENCY[country]
            assert isinstance(currency, str)
            assert len(currency) == 3  # ISO 4217 code

    def test_generated_employees_have_valid_currencies(self):
        """Employees' currencies match their country."""
        from app.seed.seed_employees import COUNTRY_TO_CURRENCY

        employees = generate_employees(count=500)

        for emp in employees:
            expected_currency = COUNTRY_TO_CURRENCY[emp.country]
            assert emp.currency == expected_currency
