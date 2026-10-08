"""Generate deterministic employee seed data for development and testing."""

import random
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List

from app.domain.employee import Employee, EmploymentType, EmployeeStatus


# Realistic geographic and organizational data
COUNTRIES = ["US", "GB", "DE", "FR", "IN", "AU", "CA", "JP", "SE"]

DEPARTMENTS = [
    "Engineering",
    "Product",
    "Sales",
    "Marketing",
    "HR",
]

JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Engineering Manager",
    "Product Manager",
    "Sales Executive",
    "Data Analyst",
    "DevOps Engineer",
    "UX Designer",
    "Business Analyst",
    "Human Resources Manager",
]

# Currency per country (ISO 4217)
COUNTRY_TO_CURRENCY = {
    "US": "USD",
    "GB": "GBP",
    "DE": "EUR",
    "FR": "EUR",
    "IN": "INR",
    "AU": "AUD",
    "CA": "CAD",
    "JP": "JPY",
    "SE": "SEK",
}

# Salary base ranges by title (in USD equivalent)
TITLE_SALARY_RANGES = {
    "Software Engineer": (80_000, 120_000),
    "Senior Software Engineer": (130_000, 180_000),
    "Engineering Manager": (140_000, 200_000),
    "Product Manager": (100_000, 160_000),
    "Sales Executive": (70_000, 150_000),
    "Data Analyst": (70_000, 110_000),
    "DevOps Engineer": (90_000, 140_000),
    "UX Designer": (75_000, 130_000),
    "Business Analyst": (65_000, 110_000),
    "Human Resources Manager": (60_000, 120_000),
}

# Country cost-of-living multipliers (relative to USD)
COUNTRY_MULTIPLIERS = {
    "US": 1.0,
    "GB": 0.95,
    "DE": 0.85,
    "FR": 0.85,
    "IN": 0.25,
    "AU": 0.95,
    "CA": 0.95,
    "JP": 0.90,
    "SE": 0.95,
}


def get_realistic_salary_for_title(title: str, country: str, rng: random.Random = None) -> Decimal:
    """
    Generate a realistic salary for a job title in a specific country.

    Salaries vary by title and country cost-of-living.
    """
    if rng is None:
        rng = random.Random()

    if title not in TITLE_SALARY_RANGES:
        title = "Software Engineer"  # Default fallback

    min_sal, max_sal = TITLE_SALARY_RANGES[title]
    multiplier = COUNTRY_MULTIPLIERS.get(country, 1.0)

    # Add some randomness within the range
    base_salary = rng.uniform(min_sal, max_sal)
    adjusted_salary = base_salary * multiplier

    # Round to nearest 100 for realism
    salary_rounded = round(adjusted_salary / 100) * 100

    return Decimal(str(salary_rounded))


def generate_employees(
    count: int = 10000,
    seed: int = 42,
) -> List[Employee]:
    """
    Generate deterministic employee data.

    Args:
        count: Number of employees to generate (default: 10,000)
        seed: Random seed for reproducibility (default: 42)

    Returns:
        List of Employee domain objects with realistic data
    """
    rng = random.Random(seed)
    employees: List[Employee] = []

    # Common first and last names for variety
    first_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
        "Iris", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Peter",
        "Quinn", "Rachel", "Sam", "Tina", "Uma", "Victor", "Wendy", "Xavier",
        "Yara", "Zara", "James", "Jennifer", "Michael", "Jessica",
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Perez", "Lee", "Thompson", "White", "Harris", "Sanchez", "Clark",
        "Ramirez", "Lewis", "Robinson",
    ]

    departments = DEPARTMENTS
    job_titles = JOB_TITLES
    countries = COUNTRIES

    # Track used emails to ensure uniqueness
    used_emails = set()

    # Hire date range: last 5 years
    today = datetime.now().date()
    five_years_ago = today - timedelta(days=5*365)

    for i in range(count):
        # Distribute employees across countries somewhat evenly
        country = countries[i % len(countries)]

        # Assign department with some weighting
        department = rng.choice(departments)

        # Assign job title
        job_title = rng.choice(job_titles)

        # Generate unique email
        first_name = rng.choice(first_names)
        last_name = rng.choice(last_names)

        email_base = f"{first_name.lower()}.{last_name.lower()}{i}@acme.com"
        while email_base in used_emails:
            email_base = f"{first_name.lower()}.{last_name.lower()}{i}_{rng.randint(1000, 9999)}@acme.com"
        used_emails.add(email_base)

        # Generate name
        name = f"{first_name} {last_name}"

        # Random hire date in last 5 years
        days_offset = rng.randint(0, 5*365)
        hire_date = five_years_ago + timedelta(days=days_offset)

        # Employment type distribution: 80% full-time, 15% part-time, 5% contract
        rand_emp_type = rng.random()
        if rand_emp_type < 0.80:
            employment_type = EmploymentType.FULL_TIME
        elif rand_emp_type < 0.95:
            employment_type = EmploymentType.PART_TIME
        else:
            employment_type = EmploymentType.CONTRACT

        # Get currency for country
        currency = COUNTRY_TO_CURRENCY[country]

        # Generate realistic salary
        salary = get_realistic_salary_for_title(job_title, country, rng)

        # Create employee
        employee = Employee(
            name=name,
            email=email_base,
            job_title=job_title,
            department=department,
            country=country,
            employment_type=employment_type,
            hire_date=hire_date,
            salary=salary,
            currency=currency,
            status=EmployeeStatus.ACTIVE,
        )

        employees.append(employee)

    return employees


def main() -> None:
    """Seed script runner."""
    import time
    from app.database import SessionLocal, engine
    from app.models import Base, EmployeeModel

    print("🌱 Starting employee seeding...")
    start_time = time.time()

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Generate seed data
    employees = generate_employees(count=10_000, seed=42)
    generation_time = time.time()
    print(f"✅ Generated {len(employees)} employees in {generation_time - start_time:.2f}s")

    # Persist to database
    db = SessionLocal()
    try:
        # Clear existing employees (optional)
        db.query(EmployeeModel).delete()
        db.commit()

        # Batch insert
        batch_size = 500
        for i in range(0, len(employees), batch_size):
            batch = employees[i:i+batch_size]
            models = [
                EmployeeModel(
                    name=emp.name,
                    email=emp.email,
                    job_title=emp.job_title,
                    department=emp.department,
                    country=emp.country,
                    employment_type=emp.employment_type,
                    hire_date=emp.hire_date,
                    salary=emp.salary,
                    currency=emp.currency,
                    status=emp.status,
                )
                for emp in batch
            ]
            db.add_all(models)
            db.commit()

        persist_time = time.time()
        print(f"✅ Persisted to database in {persist_time - generation_time:.2f}s")
        print(f"⏱️  Total time: {persist_time - start_time:.2f}s")

        # Verify
        count = db.query(EmployeeModel).count()
        print(f"✅ Database now contains {count} employees")

    finally:
        db.close()


if __name__ == "__main__":
    main()
