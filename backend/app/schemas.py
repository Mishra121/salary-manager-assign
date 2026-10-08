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
