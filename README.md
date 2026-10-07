# Salary Management System

A web-based salary management platform for HR managers to centralize employee salary data, track compensation changes, and derive actionable insights on organizational pay equity and compensation strategy.

---

## 🎯 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional, for Postgres)

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
pytest -q  # Run tests
python -m app.main  # Start dev server on http://localhost:8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev  # Start dev server on http://localhost:5173
```

#### Seed Database
```bash
cd backend
python -m app.seed  # Seeds 10,000 employees into the database
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

## 📊 Features

### Core
- ✅ Employee CRUD (create, read, update, delete)
- ✅ List/Search/Filter/Sort employees
- ✅ Salary change history tracking
- ✅ Bulk seeding (10,000 employees)

### Analytics
- ✅ Organization-wide salary KPIs (headcount, payroll, avg/median)
- ✅ Pay analysis by country, department, job title
- ✅ Salary distribution visualization
- ✅ Outlier detection (pay equity)

### Non-Features (Deliberately Left Out)
- Payroll, tax, and payslips (outside scope)
- Authentication and multi-user roles (MVP is single HR persona)
- Approval workflows (HR has authority)
- In-product AI natural-language queries (AI shown in workflow, not product)
- CSV/Excel import (manual CRUD or API seeding)

See [Requirements](docs/requirements.md) for full details.

---

## 🧪 Testing

### Run All Tests
```bash
cd backend
pytest -q
```

### Test Coverage
```bash
pytest --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm run test
```

### Performance Test (10k rows)
```bash
cd backend
pytest -m slow -v  # Benchmarks with seeded data
```

---

## 🚀 Deployment

### Render.com
1. Push to GitHub
2. Connect repo to Render
3. Set `ENVIRONMENT=production`
4. Render auto-builds and deploys from `Dockerfile`
5. Attach managed Postgres database
6. Run seed script: `python -m app.seed`

### Railway.app
Similar setup; see [Railway docs](https://docs.railway.app).

**Live Demo:** [Link TBD after deployment]

---

## 📹 Demo

A 2-3 minute video walkthrough is available [here TBD] covering:
- Requirements and product thinking
- Live demo: employee list, search, salary history, insights
- Test suite and CI/CD
- AI workflow and development approach

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
