"""API routes for salary insights and analytics."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.insights_repository import InsightsRepository
from app.services.insights_service import InsightsService
from app.schemas import (
    HeadlineKPIs,
    SalaryByCountry,
    SalaryByDepartment,
    SalaryByJobTitle,
    SalaryDistributionBucket,
    SalaryOutlier,
    InsightsResponse,
)

router = APIRouter(prefix="/insights", tags=["insights"])


def get_insights_service(db: Session = Depends(get_db)) -> InsightsService:
    """Get insights service with repository."""
    repo = InsightsRepository(db)
    return InsightsService(repo)


@router.get("/headline", response_model=HeadlineKPIs)
def get_headline_kpis(
    country: str = Query(None, description="Filter by country code"),
    department: str = Query(None, description="Filter by department"),
    job_title: str = Query(None, description="Filter by job title"),
    service: InsightsService = Depends(get_insights_service),
) -> HeadlineKPIs:
    """
    Get headline key performance indicators.

    - **headcount**: Total number of employees
    - **total_payroll_usd**: Sum of all salaries in USD
    - **average_salary_usd**: Mean salary in USD
    - **median_salary_usd**: Median salary in USD
    - **min_salary_usd**: Lowest salary in USD
    - **max_salary_usd**: Highest salary in USD

    Optional filters:
    - **country**: Filter by country code (e.g., "US")
    - **department**: Filter by department name
    - **job_title**: Filter by job title
    """
    kpis = service.get_headline_kpis(country=country, department=department, job_title=job_title)
    return HeadlineKPIs(**kpis)


@router.get("/by-country", response_model=list[SalaryByCountry])
def get_salary_by_country(
    service: InsightsService = Depends(get_insights_service),
) -> list[SalaryByCountry]:
    """
    Get salary statistics grouped by country.

    Returns headcount and salary stats (min/avg/median/max) for each country.
    """
    by_country = service.get_salary_by_country()
    return [SalaryByCountry(**data) for data in by_country]


@router.get("/by-department", response_model=list[SalaryByDepartment])
def get_salary_by_department(
    service: InsightsService = Depends(get_insights_service),
) -> list[SalaryByDepartment]:
    """
    Get salary statistics grouped by department.

    Returns headcount and salary stats (min/avg/median/max) for each department.
    """
    by_dept = service.get_salary_by_department()
    return [SalaryByDepartment(**data) for data in by_dept]


@router.get("/by-job-title", response_model=list[SalaryByJobTitle])
def get_salary_by_job_title(
    service: InsightsService = Depends(get_insights_service),
) -> list[SalaryByJobTitle]:
    """
    Get salary statistics grouped by job title.

    Returns headcount and salary stats (min/avg/median/max) for each job title.
    """
    by_title = service.get_salary_by_job_title()
    return [SalaryByJobTitle(**data) for data in by_title]


@router.get("/distribution", response_model=list[SalaryDistributionBucket])
def get_salary_distribution(
    buckets: int = Query(10, ge=5, le=50, description="Number of histogram buckets"),
    service: InsightsService = Depends(get_insights_service),
) -> list[SalaryDistributionBucket]:
    """
    Get salary distribution histogram.

    Breaks the salary range into buckets and counts employees in each.

    - **buckets**: Number of histogram buckets (default: 10, range: 5-50)
    """
    distribution = service.get_salary_distribution(bucket_count=buckets)
    return [SalaryDistributionBucket(**data) for data in distribution]


@router.get("/outliers", response_model=list[SalaryOutlier])
def get_salary_outliers(
    threshold: float = Query(2.0, ge=1.0, le=4.0, description="Standard deviation threshold"),
    service: InsightsService = Depends(get_insights_service),
) -> list[SalaryOutlier]:
    """
    Get salary outliers within job titles.

    Identifies employees with salaries significantly different from their job title's median.
    Useful for pay equity analysis and anomaly detection.

    - **threshold**: Standard deviation threshold (default: 2.0, range: 1.0-4.0)
      - 2.0 = ~95% of employees within range
      - 3.0 = ~99.7% of employees within range
    """
    outliers = service.get_salary_outliers_by_title(std_dev_threshold=threshold)
    return [SalaryOutlier(**data) for data in outliers]


@router.get("/dashboard", response_model=InsightsResponse)
def get_insights_dashboard(
    service: InsightsService = Depends(get_insights_service),
) -> InsightsResponse:
    """
    Get complete insights dashboard.

    Comprehensive view including:
    - Headline KPIs (headcount, payroll, salary stats)
    - Salary statistics by country, department, and job title
    - Salary distribution histogram
    - Outliers for pay equity analysis
    """
    headline = service.get_headline_kpis()
    by_country = service.get_salary_by_country()
    by_dept = service.get_salary_by_department()
    by_title = service.get_salary_by_job_title()
    distribution = service.get_salary_distribution()
    outliers = service.get_salary_outliers_by_title()

    return InsightsResponse(
        headline=HeadlineKPIs(**headline),
        by_country=[SalaryByCountry(**data) for data in by_country],
        by_department=[SalaryByDepartment(**data) for data in by_dept],
        by_job_title=[SalaryByJobTitle(**data) for data in by_title],
        distribution=[SalaryDistributionBucket(**data) for data in distribution],
        outliers=[SalaryOutlier(**data) for data in outliers],
    )
