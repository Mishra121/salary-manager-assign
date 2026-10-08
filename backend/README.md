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

### Development Server

```bash
# Using uv run
uv run python -m app.main

# Or run with uvicorn directly
uv run uvicorn app.main:app --reload
```

Server starts at `http://localhost:8000`

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

### Run All Tests

```bash
# Using uv run
uv run pytest -q
```

### Run Tests with Coverage

```bash
uv run pytest --cov=app --cov-report=html
```

### Run Specific Tests

```bash
# Health check test only
uv run pytest tests/test_health.py -v

# Skip slow tests
uv run pytest -m "not slow"
```

### Test Markers

- `@pytest.mark.slow` - Long-running tests (seed, performance)
- `@pytest.mark.integration` - Integration tests

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

## Database Migrations

```bash
# Generate a new migration
uv run alembic revision --autogenerate -m "add table"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1
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
