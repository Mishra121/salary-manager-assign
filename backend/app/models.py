"""SQLAlchemy ORM models for database persistence."""

from datetime import datetime, date
from decimal import Decimal

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Date,
    DateTime,
    Enum,
    Index,
    CheckConstraint,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from app.domain.employee import EmploymentType, EmployeeStatus


Base = declarative_base()


class EmployeeModel(Base):
    """SQLAlchemy ORM model for Employee entity."""

    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    job_title = Column(String(255), nullable=False, index=True)
    department = Column(String(255), nullable=False, index=True)
    country = Column(String(3), nullable=False, index=True)  # ISO 3166-1 alpha-2
    employment_type = Column(
        Enum(EmploymentType),
        nullable=False,
        default=EmploymentType.FULL_TIME,
    )
    hire_date = Column(Date, nullable=False)
    salary = Column(
        Numeric(12, 2),  # Up to 10 digits before decimal, 2 after
        nullable=False,
    )
    currency = Column(String(3), nullable=False, default="USD")
    status = Column(
        Enum(EmployeeStatus),
        nullable=False,
        default=EmployeeStatus.ACTIVE,
    )
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Constraints
    __table_args__ = (
        CheckConstraint("salary > 0", name="salary_positive"),
        UniqueConstraint("email", name="email_unique"),
        Index("idx_employees_country", "country"),
        Index("idx_employees_department", "department"),
        Index("idx_employees_job_title", "job_title"),
        Index(
            "idx_employees_country_department_title",
            "country",
            "department",
            "job_title",
        ),
    )

    def to_domain(self):
        """Convert ORM model to domain model."""
        from app.domain.employee import Employee

        return Employee(
            name=self.name,
            email=self.email,
            job_title=self.job_title,
            department=self.department,
            country=self.country,
            employment_type=self.employment_type,
            hire_date=self.hire_date,
            salary=Decimal(str(self.salary)),
            currency=self.currency,
            status=self.status,
        )

    def __repr__(self) -> str:
        """String representation."""
        return f"EmployeeModel(id={self.id}, email={self.email!r}, name={self.name!r})"


class SalaryHistoryModel(Base):
    """SQLAlchemy ORM model for tracking salary changes."""

    __tablename__ = "salary_history"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False, index=True)
    old_salary = Column(Numeric(12, 2), nullable=True)  # None if first entry
    new_salary = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    effective_date = Column(Date, nullable=False, index=True)
    reason = Column(String(255), nullable=True)  # e.g., "Annual raise", "Promotion"
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    # Constraints
    __table_args__ = (
        CheckConstraint("new_salary > 0", name="new_salary_positive"),
        Index("idx_salary_history_employee", "employee_id"),
        Index("idx_salary_history_employee_effective_date", "employee_id", "effective_date"),
    )

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"SalaryHistoryModel(id={self.id}, employee_id={self.employee_id}, "
            f"old_salary={self.old_salary}, new_salary={self.new_salary})"
        )
