"""Tests for salary insights and analytics."""

import pytest
from decimal import Decimal
from datetime import date

from app.services.insights_service import InsightsService
from app.repositories.insights_repository import InsightsRepository
from app.models import EmployeeModel


class TestHeadlineKPIs:
    """Test headline key performance indicators."""

    def test_get_headline_kpis_returns_required_fields(self, db_session):
        """Headline KPIs include headcount, payroll, and salary metrics."""
        repo = InsightsRepository(db_session)
        service = InsightsService(repo)

        kpis = service.get_headline_kpis()

        assert "headcount" in kpis
        assert "total_payroll_usd" in kpis
        assert "average_salary_usd" in kpis
        assert "median_salary_usd" in kpis
        assert "min_salary_usd" in kpis
        assert "max_salary_usd" in kpis

    def test_headline_kpis_count_employees(self, db_session):
        """Headcount includes all active employees."""
        # Add test employees
        for i in range(5):
            emp = EmployeeModel(
                name=f"Employee {i}",
                email=f"emp{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("100000"),
                currency="USD",
            )
            db_session.add(emp)
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        kpis = service.get_headline_kpis()

        assert kpis["headcount"] == 5

    def test_headline_kpis_calculate_total_payroll_usd(self, db_session):
        """Total payroll sums all salaries converted to USD."""
        # Add employees with different currencies
        emp1 = EmployeeModel(
            name="Alice", email="alice@acme.com", job_title="Engineer",
            department="Engineering", country="US",
            hire_date=date(2023, 1, 1),
            salary=Decimal("100000"), currency="USD",
        )
        emp2 = EmployeeModel(
            name="Bob", email="bob@acme.com", job_title="Engineer",
            department="Engineering", country="GB",
            hire_date=date(2023, 1, 1),
            salary=Decimal("100000"), currency="GBP",
        )
        db_session.add_all([emp1, emp2])
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        kpis = service.get_headline_kpis()

        # Payroll should sum both salaries in USD
        # 100,000 USD + (100,000 GBP * 1.25 USD/GBP) = 225,000
        assert kpis["total_payroll_usd"] > 0
        assert kpis["total_payroll_usd"] >= Decimal("200000")

    def test_headline_kpis_salary_statistics(self, db_session):
        """KPIs include min, average, max, and median salary in USD."""
        salaries = [Decimal("50000"), Decimal("75000"), Decimal("100000"), Decimal("150000")]
        for i, salary in enumerate(salaries):
            emp = EmployeeModel(
                name=f"Employee {i}",
                email=f"emp{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=salary,
                currency="USD",
            )
            db_session.add(emp)
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        kpis = service.get_headline_kpis()

        assert kpis["min_salary_usd"] == Decimal("50000")
        assert kpis["max_salary_usd"] == Decimal("150000")
        assert kpis["average_salary_usd"] == Decimal("93750")  # Sum / count
        assert kpis["median_salary_usd"] == Decimal("87500")  # Median of 4 values


class TestSalaryByDimension:
    """Test salary analysis by country, department, and job title."""

    def test_get_salary_by_country(self, db_session):
        """Salary stats aggregated by country."""
        # Add employees from two countries
        for i in range(3):
            emp = EmployeeModel(
                name=f"US Employee {i}",
                email=f"us{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("100000"),
                currency="USD",
            )
            db_session.add(emp)

        for i in range(2):
            emp = EmployeeModel(
                name=f"GB Employee {i}",
                email=f"gb{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="GB",
                hire_date=date(2023, 1, 1),
                salary=Decimal("80000"),
                currency="GBP",
            )
            db_session.add(emp)

        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        by_country = service.get_salary_by_country()

        assert len(by_country) == 2
        assert any(c["country"] == "US" for c in by_country)
        assert any(c["country"] == "GB" for c in by_country)

        us_data = next(c for c in by_country if c["country"] == "US")
        assert us_data["count"] == 3
        assert "min_salary_usd" in us_data
        assert "avg_salary_usd" in us_data
        assert "median_salary_usd" in us_data
        assert "max_salary_usd" in us_data

    def test_get_salary_by_department(self, db_session):
        """Salary stats aggregated by department."""
        for i in range(2):
            emp = EmployeeModel(
                name=f"Eng {i}",
                email=f"eng{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("100000"),
                currency="USD",
            )
            db_session.add(emp)

        for i in range(3):
            emp = EmployeeModel(
                name=f"Sales {i}",
                email=f"sales{i}@acme.com",
                job_title="Sales Rep",
                department="Sales",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("75000"),
                currency="USD",
            )
            db_session.add(emp)

        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        by_dept = service.get_salary_by_department()

        assert len(by_dept) == 2
        assert any(d["department"] == "Engineering" for d in by_dept)
        assert any(d["department"] == "Sales" for d in by_dept)

        eng_data = next(d for d in by_dept if d["department"] == "Engineering")
        assert eng_data["count"] == 2

    def test_get_salary_by_job_title(self, db_session):
        """Salary stats aggregated by job title."""
        for i in range(2):
            emp = EmployeeModel(
                name=f"Senior {i}",
                email=f"senior{i}@acme.com",
                job_title="Senior Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("150000"),
                currency="USD",
            )
            db_session.add(emp)

        for i in range(3):
            emp = EmployeeModel(
                name=f"Junior {i}",
                email=f"junior{i}@acme.com",
                job_title="Junior Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("80000"),
                currency="USD",
            )
            db_session.add(emp)

        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        by_title = service.get_salary_by_job_title()

        assert len(by_title) == 2
        senior = next(t for t in by_title if t["job_title"] == "Senior Engineer")
        assert senior["count"] == 2
        assert senior["min_salary_usd"] == Decimal("150000")


class TestSalaryDistribution:
    """Test salary distribution analysis."""

    def test_get_salary_distribution(self, db_session):
        """Salary distribution broken into histogram buckets."""
        # Add employees with varied salaries
        for salary in [30000, 50000, 75000, 100000, 125000, 150000, 200000]:
            emp = EmployeeModel(
                name=f"Employee {salary}",
                email=f"emp{salary}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal(str(salary)),
                currency="USD",
            )
            db_session.add(emp)
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        distribution = service.get_salary_distribution(bucket_count=5)

        assert len(distribution) == 5
        assert all("min" in bucket for bucket in distribution)
        assert all("max" in bucket for bucket in distribution)
        assert all("count" in bucket for bucket in distribution)

        # Total employees in all buckets should equal total added
        total_in_buckets = sum(b["count"] for b in distribution)
        assert total_in_buckets >= 7  # At least the 7 we added

    def test_salary_distribution_bucket_counts_sum_correctly(self, db_session):
        """Salary distribution buckets sum to total employees (not all in last bucket)."""
        # Create employees with specific salaries to test bucketing logic
        salaries = [10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000]
        for i, salary in enumerate(salaries):
            emp = EmployeeModel(
                name=f"Employee {i}",
                email=f"emp{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal(str(salary)),
                currency="USD",
            )
            db_session.add(emp)
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        distribution = service.get_salary_distribution(bucket_count=5)

        # Verify bucket structure
        assert len(distribution) == 5

        # Verify each bucket has proper range
        for i, bucket in enumerate(distribution):
            assert bucket["min"] < bucket["max"], f"Bucket {i}: min >= max"
            assert bucket["count"] >= 0, f"Bucket {i}: negative count"

        # CRITICAL: Sum of all bucket counts should equal total employees
        # This test catches the bug where all employees were counted in the last bucket
        total_in_buckets = sum(b["count"] for b in distribution)
        assert total_in_buckets == 10, f"Expected 10 employees total, got {total_in_buckets}. Bug: employees not distributed correctly across buckets."

        # Verify not all employees are in last bucket
        last_bucket_count = distribution[-1]["count"]
        assert last_bucket_count < 10, f"All {last_bucket_count} employees in last bucket - distribution bug!"

        # Verify first buckets have employees
        first_bucket_count = distribution[0]["count"]
        assert first_bucket_count > 0, "First bucket empty - employees not distributed!"

    def test_salary_distribution_edges(self, db_session):
        """Salary distribution handles edge cases (min/max values)."""
        # Add employees: some at min, some at max, some in middle
        min_salary = Decimal("10000")
        max_salary = Decimal("100000")

        emp_min = EmployeeModel(
            name="Low Paid",
            email="low@acme.com",
            job_title="Junior",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=min_salary,
            currency="USD",
        )
        emp_max = EmployeeModel(
            name="High Paid",
            email="high@acme.com",
            job_title="Senior",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=max_salary,
            currency="USD",
        )
        db_session.add_all([emp_min, emp_max])
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        distribution = service.get_salary_distribution(bucket_count=5)

        # Both employees should be counted
        total_in_buckets = sum(b["count"] for b in distribution)
        assert total_in_buckets == 2, "Edge case: min/max salary employees not counted"

        # First bucket should contain min_salary
        assert distribution[0]["min"] <= float(min_salary)
        # Last bucket should contain max_salary
        assert distribution[-1]["max"] >= float(max_salary)


class TestOutlierDetection:
    """Test outlier detection for pay equity analysis."""

    def test_get_salary_outliers_by_title(self, db_session):
        """Identify outliers (>2 SD from mean within job title)."""
        # Add engineers with similar salaries
        for i in range(5):
            emp = EmployeeModel(
                name=f"Engineer {i}",
                email=f"eng{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("100000"),
                currency="USD",
            )
            db_session.add(emp)

        # Add one outlier (very high salary for same title)
        outlier = EmployeeModel(
            name="High Paid Engineer",
            email="outlier@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=Decimal("250000"),
            currency="USD",
        )
        db_session.add(outlier)
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        outliers = service.get_salary_outliers_by_title()

        # Should detect the high-paid engineer as outlier
        assert len(outliers) > 0
        assert any(o["name"] == "High Paid Engineer" for o in outliers)

    def test_get_salary_outliers_includes_context(self, db_session):
        """Outliers include employee info and deviation data."""
        # Add employees
        for i in range(5):
            emp = EmployeeModel(
                name=f"Employee {i}",
                email=f"emp{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("100000"),
                currency="USD",
            )
            db_session.add(emp)

        outlier = EmployeeModel(
            name="Outlier",
            email="outlier@acme.com",
            job_title="Engineer",
            department="Engineering",
            country="US",
            hire_date=date(2023, 1, 1),
            salary=Decimal("300000"),
            currency="USD",
        )
        db_session.add(outlier)
        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)
        outliers = service.get_salary_outliers_by_title()

        for outlier_data in outliers:
            assert "name" in outlier_data
            assert "email" in outlier_data
            assert "job_title" in outlier_data
            assert "salary_usd" in outlier_data
            assert "title_median_salary_usd" in outlier_data
            assert "deviation_from_median" in outlier_data


class TestInsightsFiltering:
    """Test filtering insights by country, department, or job title."""

    def test_headline_kpis_filtered_by_country(self, db_session):
        """KPIs can be filtered to specific country."""
        # Add US employees
        for i in range(3):
            emp = EmployeeModel(
                name=f"US {i}",
                email=f"us{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="US",
                hire_date=date(2023, 1, 1),
                salary=Decimal("100000"),
                currency="USD",
            )
            db_session.add(emp)

        # Add GB employees
        for i in range(2):
            emp = EmployeeModel(
                name=f"GB {i}",
                email=f"gb{i}@acme.com",
                job_title="Engineer",
                department="Engineering",
                country="GB",
                hire_date=date(2023, 1, 1),
                salary=Decimal("80000"),
                currency="GBP",
            )
            db_session.add(emp)

        db_session.commit()

        repo = InsightsRepository(db_session)
        service = InsightsService(repo)

        # Get KPIs for US only
        us_kpis = service.get_headline_kpis(country="US")
        assert us_kpis["headcount"] == 3

        # Get KPIs for GB only
        gb_kpis = service.get_headline_kpis(country="GB")
        assert gb_kpis["headcount"] == 2
