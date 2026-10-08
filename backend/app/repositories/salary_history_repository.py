"""Repository for salary history queries and mutations."""

from decimal import Decimal
from datetime import date
from typing import List, Optional

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models import SalaryHistoryModel


class SalaryHistoryRepository:
    """Data access layer for salary history."""

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        employee_id: int,
        old_salary: Optional[Decimal],
        new_salary: Decimal,
        currency: str,
        effective_date: date,
        reason: Optional[str] = None,
    ) -> SalaryHistoryModel:
        """
        Create an immutable salary history record.

        Args:
            employee_id: ID of the employee
            old_salary: Previous salary (None for initial hire)
            new_salary: New salary amount
            currency: Currency code (e.g., 'USD')
            effective_date: Date when change became effective
            reason: Optional reason for change (e.g., 'Annual raise', 'Promotion')

        Returns:
            Created SalaryHistoryModel instance
        """
        history = SalaryHistoryModel(
            employee_id=employee_id,
            old_salary=old_salary,
            new_salary=new_salary,
            currency=currency,
            effective_date=effective_date,
            reason=reason,
        )
        self.db.add(history)
        self.db.commit()
        self.db.refresh(history)
        return history

    def get_by_employee_id(self, employee_id: int) -> List[SalaryHistoryModel]:
        """
        Get salary history for an employee, ordered by effective_date ascending.

        Args:
            employee_id: ID of the employee

        Returns:
            List of SalaryHistoryModel records in chronological order
        """
        return (
            self.db.query(SalaryHistoryModel)
            .filter(SalaryHistoryModel.employee_id == employee_id)
            .order_by(SalaryHistoryModel.effective_date.asc())
            .all()
        )

    def get_latest_by_employee_id(self, employee_id: int) -> Optional[SalaryHistoryModel]:
        """
        Get the most recent salary history record for an employee.

        Args:
            employee_id: ID of the employee

        Returns:
            Most recent SalaryHistoryModel or None if no records exist
        """
        return (
            self.db.query(SalaryHistoryModel)
            .filter(SalaryHistoryModel.employee_id == employee_id)
            .order_by(SalaryHistoryModel.effective_date.desc())
            .first()
        )

    def count_by_employee_id(self, employee_id: int) -> int:
        """
        Count salary history records for an employee.

        Args:
            employee_id: ID of the employee

        Returns:
            Number of history records
        """
        return (
            self.db.query(SalaryHistoryModel)
            .filter(SalaryHistoryModel.employee_id == employee_id)
            .count()
        )
