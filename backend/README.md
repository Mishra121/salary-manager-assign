# Salary Management System - Backend API

FastAPI-based REST API for managing employee salary data and generating compensation analytics.

## Setup

### Prerequisites
- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (modern, fast package manager)

### Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Or install only prod dependencies (without dev tools)
uv sync --no-dev
```

### Environment Configuration

```bash
cp .env.example .env
# Edit .env as needed (defaults are fine for local development)
```

## Running

### Using Make Commands (Recommended)

```bash
# From project root
make backend-start      # Seed database + start server on port 8000
make test              # Run all 75 tests
make kill-servers      # Stop running services
```

### Manual Development Server

```bash
# Seed the database first (10,000 employees, ~1 second)
uv run python -m app.seed.seed_employees

# Start server with auto-reload
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Server starts at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

## Testing

### Run All Tests (75 total, all passing ✅)

```bash
# Using make (recommended)
make test

# Or manually
uv run pytest -v        # Verbose output
uv run pytest -q        # Quick output
```

### Test Suite Breakdown

| Category | Count | Coverage |
|----------|-------|----------|
| Domain tests | 13 | Employee model, validation, currency conversion |
| Repository tests | 16 | CRUD, filtering, pagination, search |
| Service tests | 10 | Business logic, salary updates |
| Salary history tests | 8 | Timeline tracking, audit trail |
| Insights tests | 13 | KPIs, distribution, outliers, filtering |
| Seed tests | 10 | Data generation, determinism, realism |
| Health/Integration | 5 | API readiness, full flows |

### Run Tests with Coverage

```bash
uv run pytest --cov=app --cov-report=html
open htmlcov/index.html  # View coverage report
```

### Run Specific Test Files

```bash
# Test employee domain
uv run pytest tests/test_domain.py -v

# Test insights analytics
uv run pytest tests/test_insights.py -v

# Test data seeding
uv run pytest tests/test_seed.py -v
```

### Test Markers

- `@pytest.mark.slow` - Long-running tests (seed, performance)
- `@pytest.mark.integration` - Integration tests with database

## Code Quality

### Linting & Formatting

```bash
# Format code with black
uv run black .

# Check formatting
uv run black --check .

# Lint with ruff
uv run ruff check .
uv run ruff check . --fix  # Auto-fix issues

# Type checking with mypy
uv run mypy .
```

### Run All Checks

```bash
# All in one
uv run black . && uv run ruff check . && uv run mypy .
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Settings and configuration
│   ├── database.py          # SQLAlchemy setup (to be created)
│   ├── domain/              # Domain models and business logic
│   ├── api/                 # Route handlers
│   ├── services/            # Business logic layer
│   ├── repositories/        # Data access layer
│   └── tests/               # Test files
├── migrations/              # Alembic migrations (to be created)
├── tests/                   # Integration/smoke tests
├── pyproject.toml           # Dependencies and project metadata
├── pytest.ini               # Pytest configuration
├── .env.example             # Example environment variables
└── README.md                # This file
```

## Database Setup

The application uses SQLAlchemy ORM with automatic table creation on startup.

```bash
# Tables are created automatically when the app starts
# See app/main.py: Base.metadata.create_all(bind=engine)

# For development: uses SQLite (salary_management.db)
# For production: configure DATABASE_URL to Postgres connection string
```

## Development Workflow

1. Write a test that fails
2. Implement code to make it pass
3. Refactor if needed
4. Run linting and type checks
5. Commit small, atomic changes

## Documentation

- [Requirements](../docs/requirements.md) - Product requirements and scope
- [Architecture](../docs/architecture.md) - System design and tech decisions
- [Trade-offs](../docs/tradeoffs.md) - Design decisions and rationale
- [Performance](../docs/performance.md) - Benchmarks and optimizations
