# Salary Management System

A web-based salary management platform for HR managers to centralize employee salary data, track compensation changes, and derive actionable insights on organizational pay equity and compensation strategy.

---

## 🎯 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager
- Docker & Docker Compose (optional, for Postgres)

### Using Make Commands (Recommended)

```bash
# View all available commands
make help

# Run all backend tests (75 tests)
make test

# Start backend server (auto-seeds database on first run)
make backend-start

# Start frontend dev server (in another terminal)
make frontend-start

# Stop all running servers
make kill-servers
```

### Manual Setup

#### Backend
```bash
cd backend
uv sync  # Install dependencies (includes dev tools)
uv run pytest -q  # Run tests (75 total)
uv run python -m app.seed.seed_employees  # Seed 10,000 employees
uv run uvicorn app.main:app --reload  # Start dev server on http://localhost:8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev  # Start dev server on http://localhost:5173
```

### Docker

```bash
docker-compose up --build
# App available at http://localhost:8000
```

---

## 📋 Documentation

- **[Requirements](docs/requirements.md)** — Goal, scope, features, assumptions
- **[Architecture](docs/architecture.md)** — System design, DB schema, tech stack rationale
- **[Trade-offs](docs/tradeoffs.md)** — Design decisions and alternatives
- **[AI Workflow](docs/ai-workflow.md)** — How AI was used during development
- **[Performance](docs/performance.md)** — Benchmarks and optimization notes
- **[Plan](PLAN.md)** — Full execution plan and strategy

---

## 🏗️ Architecture

### Backend
- **Framework:** FastAPI
- **Database:** SQLAlchemy 2.x (SQLite in dev, Postgres in prod)
- **ORM Patterns:** Repositories, Services, Domain models
- **Testing:** pytest with factories
- **Quality:** ruff, mypy, 90%+ coverage

### Frontend
- **Framework:** React 18 + TypeScript
- **Build:** Vite
- **State:** TanStack Query (data fetching)
- **Tables:** TanStack Table (pagination, sorting, filtering)
- **Charts:** Recharts
- **Components:** shadcn/ui / MUI
- **Testing:** Vitest + React Testing Library

### Deployment
- **Container:** Docker (single image, multi-stage build)
- **Platform:** Render / Railway (free tier)
- **Database:** Postgres managed service
- **CI/CD:** GitHub Actions (lint, test, deploy)

---

## 📊 Features (All Implemented ✅)

### Employee Management
- ✅ Create employee with full validation
- ✅ View employee details with salary history timeline
- ✅ Edit employee information
- ✅ Delete employee records
- ✅ List employees with server-side pagination (50/page)
- ✅ Search by name, email, or job title
- ✅ Filter by country, department, employment type
- ✅ Multi-currency support (USD, GBP, EUR, INR, AUD, CAD, JPY, SEK)

### Salary Analytics
- ✅ Salary change history with timeline view
- ✅ Automatic salary history tracking on every update
- ✅ Immutable audit trail of all salary changes

### Insights Dashboard
- ✅ Organization-wide KPIs: headcount, total payroll (USD), avg/median salary
- ✅ Salary statistics by country (9 countries)
- ✅ Salary statistics by department (5 departments)
- ✅ Salary statistics by job title (10+ titles)
- ✅ Salary distribution histogram (10 buckets)
- ✅ Outlier detection (>2 SD from title median)
- ✅ Interactive charts with Recharts
- ✅ Custom tooltips showing salary ranges
- ✅ Min/max salary range cards

### Data & Performance
- ✅ Bulk seeding: 10,000 deterministic employees in <1 second
- ✅ Database queries: <300ms for 10k rows
- ✅ Multi-currency salary conversion
- ✅ Server-side pagination for scalability

### Non-Features (Deliberately Left Out)
- Payroll, tax, and payslips (outside scope)
- Authentication and multi-user roles (MVP is single HR persona)
- Approval workflows (HR has authority)
- In-product AI natural-language queries (AI shown in workflow, not product)
- CSV/Excel import (manual CRUD or API seeding)

See [Requirements](docs/requirements.md) for full details.

---

## 🧪 Testing

### Backend Tests (75 total, all passing ✅)
```bash
# Using make (recommended)
make test

# Or manually
cd backend
uv run pytest -v  # Verbose output
uv run pytest -q  # Quick output
```

### Test Coverage
```bash
cd backend
uv run pytest --cov=app --cov-report=html
```

### Test Breakdown
- **Domain tests**: Employee validation, currency conversion (13 tests)
- **Repository tests**: CRUD, filtering, pagination (16 tests)
- **Service tests**: Business logic (10 tests)
- **Salary history tests**: Tracking and timelines (8 tests)
- **Insights tests**: KPIs, distribution, outliers (13 tests)
- **Seed tests**: Data generation, determinism (10 tests)
- **Health check test**: API readiness (1 test)
- **Integration tests**: Full API flows (4 tests)

### Frontend Tests
```bash
cd frontend
npm run test
```

### Performance Verification (10k rows)
```bash
cd backend
uv run pytest tests/test_seed.py -v  # Seeding benchmark
```

---

## 🚀 Deployment

### Render.com (Recommended)
1. Fork/push repo to GitHub
2. Create new Web Service on Render
3. Connect to your GitHub repository
4. Set environment variables:
   - `ENVIRONMENT=production`
   - `DATABASE_URL=postgresql://...` (use Render Postgres)
5. Build command: `cd backend && uv sync && uv run python -m app.seed.seed_employees`
6. Start command: `cd backend && uv run uvicorn app.main:app --host 0.0.0.0 --port 8000`
7. Connect Postgres database from Render dashboard
8. Deploy!

### Railway.app
Similar process; see [Railway docs](https://docs.railway.app) for detailed setup.

### Docker Local
```bash
docker-compose up --build
```

---

## 📚 Development Notes

### Git Workflow
Each commit should be small and atomic:
- Test commit: failing test for a feature
- Implementation commit: make the test green
- Refactor commit (optional): cleanup without changing behavior

View the full git history: `git log --oneline`

### Code Quality
- Run before every commit:
  ```bash
  ruff check . && mypy . && black . && pytest -q
  ```
- CI will block PRs if these fail

### Adding a New Feature
1. Write a test (e.g., `test_new_feature`)
2. Implement to make it green
3. Commit: `feat: add new feature`
4. Repeat for each slice

---

## 🤖 AI Development Workflow

This project was built using Claude AI as a collaborative tool. See [AI Workflow](docs/ai-workflow.md) for:
- Prompts used
- What AI got right and wrong
- Manual corrections applied
- Learned lessons

---

## 📝 Git History

The commit history is designed to tell the story of development:
- `chore:` scaffolding and setup
- `docs:` requirements, architecture, notes
- `test:` failing tests
- `feat:` feature implementation
- `refactor:` code cleanup without behavior change
- `perf:` performance improvements

Example:
```
6a3c2f1 (HEAD) docs: add performance benchmarks and deployment guide
8e4d9c2 video: record 2-3 min demo walkthrough
5f7b3c8 test: assert insights queries <500ms on 10k rows
2a8f6c1 feat: add salary distribution histogram chart
9d2e1f5 feat: add insights dashboard with KPI cards
...
1c5e3a9 test: first failing test for health check endpoint
4b7e2c6 chore: initialize fastapi backend scaffold
3a9f1d2 docs: commit requirements.md (product thinking first)
a2e4f8c chore: repo init with plan and .gitignore
```

---

**Questions?** Refer to [PLAN.md](PLAN.md) for the execution strategy or [Architecture](docs/architecture.md) for technical details.
