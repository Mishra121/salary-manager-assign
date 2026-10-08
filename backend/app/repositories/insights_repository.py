"""Repository for salary insights and analytics queries."""

from decimal import Decimal
from typing import List, Optional, Dict, Any

from sqlalchemy import func, desc, case
from sqlalchemy.orm import Session

from app.models import EmployeeModel
from app.domain.currency import CurrencyConverter


class InsightsRepository:
    """Data access layer for insights queries."""

    def __init__(self, db: Session):
        self.db = db
        self.converter = CurrencyConverter()

    def get_headline_kpis(
        self,
        country: Optional[str] = None,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get headline key performance indicators.

        Returns:
            Dict with headcount, total_payroll_usd, and salary statistics (all in USD).
        """
        query = self.db.query(EmployeeModel)

        if country:
            query = query.filter(EmployeeModel.country == country)
        if department:
            query = query.filter(EmployeeModel.department == department)
        if job_title:
            query = query.filter(EmployeeModel.job_title == job_title)

        employees = query.all()

        if not employees:
            return {
                "headcount": 0,
                "total_payroll_usd": Decimal("0"),
                "average_salary_usd": Decimal("0"),
                "median_salary_usd": Decimal("0"),
                "min_salary_usd": Decimal("0"),
                "max_salary_usd": Decimal("0"),
            }

        # Convert all salaries to USD
        salaries_usd = [
            self.converter.convert(emp.salary, emp.currency, "USD")
            for emp in employees
        ]

        salaries_usd.sort()

        total_payroll = sum(salaries_usd)
        avg_salary = total_payroll / len(salaries_usd)

        # Calculate median
        mid = len(salaries_usd) // 2
        if len(salaries_usd) % 2 == 0:
            median_salary = (salaries_usd[mid - 1] + salaries_usd[mid]) / 2
        else:
            median_salary = salaries_usd[mid]

        return {
            "headcount": len(employees),
            "total_payroll_usd": round(total_payroll, 2),
            "average_salary_usd": round(avg_salary, 2),
            "median_salary_usd": round(median_salary, 2),
            "min_salary_usd": round(salaries_usd[0], 2),
            "max_salary_usd": round(salaries_usd[-1], 2),
        }

    def get_salary_by_country(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics grouped by country.

        Returns:
            List of dicts with country, count, and salary stats in USD.
        """
        countries = self.db.query(EmployeeModel.country).distinct().all()

        results = []
        for (country,) in countries:
            employees = (
                self.db.query(EmployeeModel)
                .filter(EmployeeModel.country == country)
                .all()
            )

            if employees:
                salaries_usd = [
                    self.converter.convert(emp.salary, emp.currency, "USD")
                    for emp in employees
                ]
                salaries_usd.sort()

                results.append({
                    "country": country,
                    "count": len(employees),
                    "min_salary_usd": round(salaries_usd[0], 2),
                    "avg_salary_usd": round(sum(salaries_usd) / len(salaries_usd), 2),
                    "median_salary_usd": self._calculate_median(salaries_usd),
                    "max_salary_usd": round(salaries_usd[-1], 2),
                })

        return sorted(results, key=lambda x: x["count"], reverse=True)

    def get_salary_by_department(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics grouped by department.

        Returns:
            List of dicts with department, count, and salary stats in USD.
        """
        departments = self.db.query(EmployeeModel.department).distinct().all()

        results = []
        for (dept,) in departments:
            employees = (
                self.db.query(EmployeeModel)
                .filter(EmployeeModel.department == dept)
                .all()
            )

            if employees:
                salaries_usd = [
                    self.converter.convert(emp.salary, emp.currency, "USD")
                    for emp in employees
                ]
                salaries_usd.sort()

                results.append({
                    "department": dept,
                    "count": len(employees),
                    "min_salary_usd": round(salaries_usd[0], 2),
                    "avg_salary_usd": round(sum(salaries_usd) / len(salaries_usd), 2),
                    "median_salary_usd": self._calculate_median(salaries_usd),
                    "max_salary_usd": round(salaries_usd[-1], 2),
                })

        return sorted(results, key=lambda x: x["count"], reverse=True)

    def get_salary_by_job_title(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics grouped by job title.

        Returns:
            List of dicts with job_title, count, and salary stats in USD.
        """
        titles = self.db.query(EmployeeModel.job_title).distinct().all()

        results = []
        for (title,) in titles:
            employees = (
                self.db.query(EmployeeModel)
                .filter(EmployeeModel.job_title == title)
                .all()
            )

            if employees:
                salaries_usd = [
                    self.converter.convert(emp.salary, emp.currency, "USD")
                    for emp in employees
                ]
                salaries_usd.sort()

                results.append({
                    "job_title": title,
                    "count": len(employees),
                    "min_salary_usd": round(salaries_usd[0], 2),
                    "avg_salary_usd": round(sum(salaries_usd) / len(salaries_usd), 2),
                    "median_salary_usd": self._calculate_median(salaries_usd),
                    "max_salary_usd": round(salaries_usd[-1], 2),
                })

        return sorted(results, key=lambda x: x["count"], reverse=True)

    def get_salary_distribution(self, bucket_count: int = 10) -> List[Dict[str, Any]]:
        """
        Get salary distribution broken into histogram buckets.

        Args:
            bucket_count: Number of buckets for histogram (default: 10)

        Returns:
            List of buckets with min, max, and employee count.
        """
        all_employees = self.db.query(EmployeeModel).all()

        if not all_employees:
            return []

        # Convert all to USD
        salaries_usd = [
            self.converter.convert(emp.salary, emp.currency, "USD")
            for emp in all_employees
        ]

        min_sal = min(salaries_usd)
        max_sal = max(salaries_usd)

        if min_sal == max_sal:
            return [{
                "min": float(min_sal),
                "max": float(max_sal),
                "count": len(salaries_usd),
            }]

        bucket_size = (max_sal - min_sal) / bucket_count
        buckets = []

        for i in range(bucket_count):
            bucket_min = min_sal + (i * bucket_size)
            bucket_max = min_sal + ((i + 1) * bucket_size)

            # Count employees in this bucket
            if i == bucket_count - 1:
                # Last bucket: include upper boundary to catch any floating point edge cases
                count = sum(1 for sal in salaries_usd if bucket_min <= sal <= bucket_max)
            else:
                # Other buckets: exclude upper boundary to avoid double-counting
                count = sum(1 for sal in salaries_usd if bucket_min <= sal < bucket_max)

            buckets.append({
                "min": float(round(bucket_min, 2)),
                "max": float(round(bucket_max, 2)),
                "count": count,
            })

        return buckets

    def get_salary_outliers_by_title(self, std_dev_threshold: float = 2.0) -> List[Dict[str, Any]]:
        """
        Identify salary outliers (employees deviating >threshold std devs from title median).

        Args:
            std_dev_threshold: Number of standard deviations to consider outlier (default: 2.0)

        Returns:
            List of outlier employees with context.
        """
        titles = self.db.query(EmployeeModel.job_title).distinct().all()
        outliers = []

        for (title,) in titles:
            employees = (
                self.db.query(EmployeeModel)
                .filter(EmployeeModel.job_title == title)
                .all()
            )

            if len(employees) < 3:  # Need at least 3 to identify outliers
                continue

            # Convert to USD
            salaries_by_emp = {
                emp: self.converter.convert(emp.salary, emp.currency, "USD")
                for emp in employees
            }

            salaries_usd = list(salaries_by_emp.values())
            salaries_usd.sort()

            # Calculate median and std dev
            median = self._calculate_median(salaries_usd)
            variance = sum((s - median) ** 2 for s in salaries_usd) / len(salaries_usd)
            std_dev = float(variance) ** 0.5

            if std_dev == 0:
                continue

            # Identify outliers
            for emp, sal_usd in salaries_by_emp.items():
                deviation = abs(float(sal_usd) - float(median)) / std_dev if std_dev > 0 else 0
                if deviation > std_dev_threshold:
                    outliers.append({
                        "id": emp.id,
                        "name": emp.name,
                        "email": emp.email,
                        "job_title": emp.job_title,
                        "department": emp.department,
                        "country": emp.country,
                        "salary_usd": round(sal_usd, 2),
                        "title_median_salary_usd": round(median, 2),
                        "deviation_from_median": round((sal_usd - median) / median * 100, 1),  # Percentage
                    })

        return sorted(outliers, key=lambda x: x["deviation_from_median"], reverse=True)

    def _calculate_median(self, sorted_values: List[Decimal]) -> Decimal:
        """Calculate median of sorted list."""
        if not sorted_values:
            return Decimal("0")

        mid = len(sorted_values) // 2
        if len(sorted_values) % 2 == 0:
            return (sorted_values[mid - 1] + sorted_values[mid]) / 2
        else:
            return sorted_values[mid]
