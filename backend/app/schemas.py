"""Pydantic schemas for request/response validation."""

from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.domain.employee import EmploymentType, EmployeeStatus


class EmployeeBase(BaseModel):
    """Base schema with common employee fields."""

    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    job_title: str = Field(..., min_length=1, max_length=255)
    department: str = Field(..., min_length=1, max_length=255)
    country: str = Field(..., min_length=2, max_length=3)
    employment_type: EmploymentType
    hire_date: date
    salary: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(default="USD", min_length=3, max_length=3)
    status: EmployeeStatus = Field(default=EmployeeStatus.ACTIVE)


class EmployeeCreate(EmployeeBase):
    """Schema for creating employee."""

    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating employee (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    job_title: Optional[str] = Field(None, min_length=1, max_length=255)
    department: Optional[str] = Field(None, min_length=1, max_length=255)
    country: Optional[str] = Field(None, min_length=2, max_length=3)
    employment_type: Optional[EmploymentType] = None
    hire_date: Optional[date] = None
    salary: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    currency: Optional[str] = Field(None, min_length=3, max_length=3)
    status: Optional[EmployeeStatus] = None


class EmployeeResponse(EmployeeBase):
    """Schema for employee response."""

    id: int

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    """Schema for paginated employee list response."""

    total: int = Field(..., description="Total count of matching employees")
    skip: int = Field(..., ge=0, description="Number of records skipped")
    limit: int = Field(..., gt=0, description="Limit of records returned")
    employees: list[EmployeeResponse]


class ListQueryParams(BaseModel):
    """Schema for common list query parameters."""

    skip: int = Field(default=0, ge=0, description="Number of records to skip")
    limit: int = Field(default=50, gt=0, le=200, description="Number of records to return")
    search: Optional[str] = Field(None, description="Search by name or email")
    country: Optional[str] = Field(None, description="Filter by country")
    department: Optional[str] = Field(None, description="Filter by department")
    job_title: Optional[str] = Field(None, description="Filter by job title")


class HeadlineKPIs(BaseModel):
    """Headline key performance indicators."""

    headcount: int = Field(..., description="Total number of employees")
    total_payroll_usd: Decimal = Field(..., description="Total payroll in USD")
    average_salary_usd: Decimal = Field(..., description="Average salary in USD")
    median_salary_usd: Decimal = Field(..., description="Median salary in USD")
    min_salary_usd: Decimal = Field(..., description="Minimum salary in USD")
    max_salary_usd: Decimal = Field(..., description="Maximum salary in USD")


class SalaryStatsByDimension(BaseModel):
    """Salary statistics for a dimension (country, department, or job title)."""

    count: int = Field(..., description="Number of employees")
    min_salary_usd: Decimal = Field(..., description="Minimum salary in USD")
    avg_salary_usd: Decimal = Field(..., description="Average salary in USD")
    median_salary_usd: Decimal = Field(..., description="Median salary in USD")
    max_salary_usd: Decimal = Field(..., description="Maximum salary in USD")


class SalaryByCountry(SalaryStatsByDimension):
    """Salary stats by country."""

    country: str = Field(..., description="Country code")


class SalaryByDepartment(SalaryStatsByDimension):
    """Salary stats by department."""

    department: str = Field(..., description="Department name")


class SalaryByJobTitle(SalaryStatsByDimension):
    """Salary stats by job title."""

    job_title: str = Field(..., description="Job title")


class SalaryDistributionBucket(BaseModel):
    """One bucket in salary distribution histogram."""

    min: float = Field(..., description="Bucket minimum salary (USD)")
    max: float = Field(..., description="Bucket maximum salary (USD)")
    count: int = Field(..., description="Number of employees in bucket")


class SalaryOutlier(BaseModel):
    """Outlier employee with salary context."""

    id: int = Field(..., description="Employee ID")
    name: str = Field(..., description="Employee name")
    email: str = Field(..., description="Employee email")
    job_title: str = Field(..., description="Job title")
    department: str = Field(..., description="Department")
    country: str = Field(..., description="Country code")
    salary_usd: Decimal = Field(..., description="Salary in USD")
    title_median_salary_usd: Decimal = Field(..., description="Median salary for this title")
    deviation_from_median: float = Field(..., description="Percentage deviation from title median")


class InsightsResponse(BaseModel):
    """Complete insights dashboard response."""

    headline: HeadlineKPIs
    by_country: list[SalaryByCountry]
    by_department: list[SalaryByDepartment]
    by_job_title: list[SalaryByJobTitle]
    distribution: list[SalaryDistributionBucket]
    outliers: list[SalaryOutlier]
