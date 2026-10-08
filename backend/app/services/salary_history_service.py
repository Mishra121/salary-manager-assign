"""Service for salary history business logic."""

from decimal import Decimal
from datetime import date
from typing import List, Optional, Dict, Any

from app.repositories.salary_history_repository import SalaryHistoryRepository


class SalaryHistoryService:
    """Business logic for salary history tracking."""

    def __init__(self, repo: SalaryHistoryRepository):
        self.repo = repo

    def record_salary_change(
        self,
        employee_id: int,
        old_salary: Optional[Decimal],
        new_salary: Decimal,
        currency: str,
        effective_date: date,
        reason: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Record a salary change for an employee.

        Args:
            employee_id: ID of the employee
            old_salary: Previous salary (None for initial hire)
            new_salary: New salary amount
            currency: Currency code
            effective_date: When the change takes effect
            reason: Why the change was made

        Returns:
            Dict with recorded history details
        """
        history = self.repo.create(
            employee_id=employee_id,
            old_salary=old_salary,
            new_salary=new_salary,
            currency=currency,
            effective_date=effective_date,
            reason=reason,
        )

        return {
            "id": history.id,
            "employee_id": history.employee_id,
            "old_salary": history.old_salary,
            "new_salary": history.new_salary,
            "currency": history.currency,
            "effective_date": history.effective_date,
            "reason": history.reason,
        }

    def get_salary_history(self, employee_id: int) -> List[Dict[str, Any]]:
        """
        Get full salary history for an employee.

        Args:
            employee_id: ID of the employee

        Returns:
            List of salary history records in chronological order
        """
        records = self.repo.get_by_employee_id(employee_id)
        return [
            {
                "id": r.id,
                "employee_id": r.employee_id,
                "old_salary": r.old_salary,
                "new_salary": r.new_salary,
                "currency": r.currency,
                "effective_date": r.effective_date,
                "reason": r.reason,
            }
            for r in records
        ]

    def get_current_salary(self, employee_id: int) -> Optional[Decimal]:
        """
        Get the current salary from the most recent history record.

        Args:
            employee_id: ID of the employee

        Returns:
            Current salary or None if no history exists
        """
        latest = self.repo.get_latest_by_employee_id(employee_id)
        return latest.new_salary if latest else None

    def get_total_raise(self, employee_id: int) -> float:
        """
        Calculate total raise percentage from initial to current salary.

        Args:
            employee_id: ID of the employee

        Returns:
            Percentage increase (e.g., 50.0 for 50% raise)
        """
        records = self.repo.get_by_employee_id(employee_id)

        if not records or len(records) < 1:
            return 0.0

        initial_salary = float(records[0].new_salary)
        if initial_salary == 0:
            return 0.0

        current_salary = float(records[-1].new_salary)
        percentage = ((current_salary - initial_salary) / initial_salary) * 100

        return round(percentage, 1)

    def get_salary_timeline(self, employee_id: int) -> List[Dict[str, Any]]:
        """
        Get formatted salary timeline showing all changes.

        Args:
            employee_id: ID of the employee

        Returns:
            List of timeline entries with salary and change info
        """
        records = self.repo.get_by_employee_id(employee_id)

        timeline = []
        for i, record in enumerate(records):
            entry: Dict[str, Any] = {
                "id": record.id,
                "employee_id": record.employee_id,
                "old_salary": record.old_salary,
                "new_salary": record.new_salary,
                "currency": record.currency,
                "effective_date": record.effective_date,
                "reason": record.reason,
            }

            # Add percentage change from previous salary
            if i > 0:
                prev_salary = float(records[i - 1].new_salary)
                current_salary = float(record.new_salary)
                if prev_salary > 0:
                    change_pct = ((current_salary - prev_salary) / prev_salary) * 100
                    entry["change_percentage"] = round(change_pct, 1)

            timeline.append(entry)

        return timeline

    def get_salary_history_count(self, employee_id: int) -> int:
        """
        Get the number of salary change records for an employee.

        Args:
            employee_id: ID of the employee

        Returns:
            Count of salary history records
        """
        return self.repo.count_by_employee_id(employee_id)
