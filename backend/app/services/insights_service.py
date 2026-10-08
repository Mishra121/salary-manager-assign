"""Business logic for salary insights and analytics."""

from typing import List, Optional, Dict, Any

from app.repositories.insights_repository import InsightsRepository


class InsightsService:
    """Service for salary analytics and insights."""

    def __init__(self, repository: InsightsRepository):
        self.repository = repository

    def get_headline_kpis(
        self,
        country: Optional[str] = None,
        department: Optional[str] = None,
        job_title: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get headline key performance indicators.

        Includes: headcount, total payroll (USD), and salary statistics (min/avg/median/max).

        Args:
            country: Optional country filter
            department: Optional department filter
            job_title: Optional job title filter

        Returns:
            Dict with headline metrics in USD.
        """
        return self.repository.get_headline_kpis(country, department, job_title)

    def get_salary_by_country(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics grouped by country.

        Returns:
            List of countries with headcount and salary stats (min/avg/median/max in USD).
        """
        return self.repository.get_salary_by_country()

    def get_salary_by_department(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics grouped by department.

        Returns:
            List of departments with headcount and salary stats (min/avg/median/max in USD).
        """
        return self.repository.get_salary_by_department()

    def get_salary_by_job_title(self) -> List[Dict[str, Any]]:
        """
        Get salary statistics grouped by job title.

        Returns:
            List of job titles with headcount and salary stats (min/avg/median/max in USD).
        """
        return self.repository.get_salary_by_job_title()

    def get_salary_distribution(self, bucket_count: int = 10) -> List[Dict[str, Any]]:
        """
        Get salary distribution histogram.

        Breaks salary range into buckets and counts employees in each.

        Args:
            bucket_count: Number of buckets (default: 10)

        Returns:
            List of buckets with min, max, and employee count.
        """
        return self.repository.get_salary_distribution(bucket_count)

    def get_salary_outliers_by_title(self, std_dev_threshold: float = 2.0) -> List[Dict[str, Any]]:
        """
        Identify salary outliers within job titles.

        Employees with salaries >threshold standard deviations from their title's median.
        Useful for pay equity analysis and anomaly detection.

        Args:
            std_dev_threshold: Standard deviation threshold (default: 2.0)

        Returns:
            List of outlier employees with salary context.
        """
        return self.repository.get_salary_outliers_by_title(std_dev_threshold)
