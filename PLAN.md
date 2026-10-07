# Salary Management System: Execution Plan

## Overview
Build a web-based salary management tool for an HR Manager at ACME Corporation (10,000 employees, multiple countries) to replace spreadsheet-based salary management with a scalable, maintainable platform.

**Core Principle:** Focus on engineering excellence:
- Clear thinking and product framing (requirements first)
- TDD discipline (test → impl → refactor pattern)
- Intentional use of AI as a development tool
- Production-quality code (performance, tests, indexes, scale-aware)
- Transparent decision-making (trade-offs documented, evolution visible in git)

**Target:** Deployed, live platform with full test coverage and comprehensive documentation.

---

## Stack Decisions
- **Backend:** FastAPI, SQLAlchemy 2.x ORM
- **Database:** SQLite locally (dev/test), PostgreSQL in prod (Render/Railway)
- **Frontend:** React + TypeScript + Vite, TanStack Query, TanStack Table
- **Component Library:** MUI (Material-UI) for faster table/form development
- **Deployment:** Single Docker image (FastAPI serves static + API), Render or Railway
- **AI as Tool:** Documented in workflow; not embedded in product features

---

## Success Criteria
1. **Requirements document** (1 page, committed first): Goal, scope, "deliberately left out" list with reasoning
2. **Visible TDD in git:** ~30-50 small conventional commits; test-first history
3. **AI workflow documented:** prompts, corrections, learnings in `docs/ai-workflow.md`
4. **Handles 10k scale:** pagination, indexes, aggregation, batch seed; timing benchmarks
5. **Working live URL + video demo** (2-3 min, Loom)
6. **Trade-offs document:** what was decided and why
7. **Clean code & tests:** ≥90% coverage on domain/services, ruff/mypy/eslint passing

---

## Design Decisions (Scope Clarity)

The following design decisions set clear boundaries for the MVP:
- **Multi-currency:** Yes, with static rate table for USD analytics (not live FX rates)
- **Salary history:** Yes, track all changes with effective dates; no approval workflows
- **Auth/RBAC:** Single HR persona, no login required (first enhancement post-MVP)
- **CSV import:** Stretch goal; MVP uses manual CRUD or API seeding

---

## Scope: MVP Features (Priority Order)

### 1. Employee CRUD
- Fields: name, email, job title, department, country, employment type, hire date, salary, currency, status
- Validations: positive salary, valid country/currency, unique email
- API: POST/GET/PUT/DELETE with validation

### 2. Employee List at Scale
- Server-side pagination (50/100/200 per page)
- Search (name, email, job title)
- Filters: country, department, job title
- Sort: any column
- Response time target: <300 ms for 10k rows

### 3. Salary Change History
- Track each salary update: old value, new value, effective date, reason
- Displayed on employee detail
- Editable (reason) but immutable (old/new values)

### 4. Insights Dashboard (Product Thinking Differentiator)
- **KPIs:** headcount, total payroll (USD), median/avg salary
- **By Segment:**
  - Min/avg/median/max/p25/p75 by country
  - Min/avg/median/max/p25/p75 by department
  - Min/avg/median/max/p25/p75 by job title
- **Distribution:** histogram/scatter of all salaries
- **Outliers:** employees >2 SD from their title's median
- **Pay Bands:** salary spread within each title/department

### 5. Seed Script
- 10,000 deterministic employees (seeded RNG)
- 8-10 countries with realistic salary distributions per country/title
- Realistic department/title mixes
- Batch insert in seconds; idempotent (re-run safe)

---

## Deliberately Left Out (with reasoning)
| Feature | Reason |
|---------|--------|
| Payroll/Tax/Payslips | Outside scope; org pays people, doesn't process payroll here |
| Auth/RBAC/SSO | Single HR persona assumed; adds deployment complexity; first enhancement post-MVP |
| Approval workflows | No sign-off needed; HR has authority; complicates state machine |
| Audit-grade compliance | Not mentioned in requirements; future if org scales |
| Live FX rates | Static rates sufficient for this assignment; live rates add API/cost/latency |
| Equity/bonus modeling | Out of scope for salary management; future feature |
| In-product AI (NL queries) | Distracts from core; AI shown in workflow/process, not product |
| CSV/Excel import | Stretch goal; manual CRUD or API seeding for assessment |

---

## Architecture

```
assign-incubyte/
├── PLAN.md                        (this file)
├── CLAUDE.md                      (AI instructions for the reviewer)
├── AGENTS.md                      (high-level AI workflow notes)
├── docs/
│   ├── requirements.md            (1 page: goal, scope, out-of-scope, assumptions)
│   ├── architecture.md            (layered design, DB schema sketch, Mermaid diagram)
│   ├── tradeoffs.md               (decisions: SQLite vs Postgres, frontend lib, etc.)
│   ├── ai-workflow.md             (prompts used, what was corrected, learnings)
│   ├── performance.md             (benchmark numbers: query times, seed time, etc.)
│   └── decisions/                 (short ADRs if needed)
├── backend/
│   ├── pyproject.toml             (Poetry or PDM)
│   ├── pytest.ini
│   ├── Dockerfile                 (multi-stage)
│   ├── alembic/                   (migrations)
│   └── app/
│       ├── __init__.py
│       ├── main.py                (FastAPI app, routes, startup)
│       ├── config.py              (settings, env vars)
│       ├── database.py            (SQLAlchemy engine, session factory)
│       ├── domain/
│       │   ├── employee.py        (Employee model, enums, validations)
│       │   ├── salary_history.py  (SalaryHistory model)
│       │   ├── currency.py        (Converter, rates table—pure functions)
│       │   └── insights.py        (Data classes for analytics, calculations)
│       ├── api/
│       │   ├── v1.py              (top-level router)
│       │   ├── employees.py       (CRUD routes)
│       │   ├── salary_history.py  (history routes)
│       │   └── insights.py        (analytics routes)
│       ├── services/
│       │   ├── employee_service.py
│       │   ├── salary_history_service.py
│       │   ├── insights_service.py
│       │   └── seed_service.py
│       ├── repositories/
│       │   ├── employee_repo.py   (queries, list/search/filter/paginate)
│       │   ├── salary_history_repo.py
│       │   └── insights_repo.py   (aggregations for analytics)
│       └── tests/
│           ├── test_domain.py     (Employee model, currency, validations)
│           ├── test_services.py   (business logic)
│           ├── test_api.py        (HTTP integration)
│           └── factories.py       (test data builders)
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── vitest.config.ts
│   ├── public/
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/                   (Axios/fetch client, queries)
│       ├── components/
│       │   ├── EmployeeTable.tsx
│       │   ├── EmployeeForm.tsx
│       │   ├── EmployeeDetail.tsx (with salary history)
│       │   ├── InsightsDashboard.tsx
│       │   ├── KPICard.tsx
│       │   ├── SalaryChart.tsx
│       │   └── FilterBar.tsx
│       ├── pages/
│       │   ├── EmployeesPage.tsx
│       │   └── InsightsPage.tsx
│       ├── hooks/
│       │   └── useEmployees.ts    (React Query hooks)
│       ├── types/
│       │   └── index.ts
│       ├── __tests__/             (Vitest + RTL)
│       │   ├── EmployeeTable.test.tsx
│       │   ├── EmployeeForm.test.tsx
│       │   └── InsightsDashboard.test.tsx
│       └── styles/                (Tailwind, component styles)
├── .github/workflows/
│   └── ci.yml                     (lint, type-check, test on every push)
├── docker-compose.yml             (local Postgres for dev, optional)
├── Dockerfile
├── .gitignore
├── README.md                      (run, test, deploy, links)
└── requirements.txt / pyproject.toml
```

**Key Design Patterns:**
- **Layered:** Router → Service → Repository → DB, so business logic is testable without HTTP/DB
- **Domain-driven:** Employee, SalaryHistory, Currency as pure domain objects with validations
- **Pagination:** cursor or offset-based, server-side only
- **Indexes:** (country), (department), (job_title), composite on filter combinations
- **Money:** stored as integer (minor units, e.g., cents), never float
- **SQL Portability:** aggregations written to work on both SQLite and Postgres; parameterized queries

---

## Execution Order (Each = ≥1 commit with tests preceding code)

### Phase 1: Foundations (Day 1 morning)
1. **chore:** git init, .gitignore, README scaffold, AGENTS.md, CLAUDE.md
2. **docs:** requirements.md (1 page, committed first), architecture.md sketch
3. **backend:** FastAPI scaffold, pyproject.toml, pytest config, GitHub Actions CI stub
4. **test:** health check endpoint (test-first), then implement
5. **domain:** Employee model + Pydantic validation (TDD)
6. **domain:** Currency conversion utilities (TDD, pure functions)

### Phase 2: Backend MVP (Day 1 afternoon)
7. **db:** SQLAlchemy models (Employee, SalaryHistory), migration
8. **api:** Employee CRUD endpoints (test-first)
9. **services:** EmployeeService, EmployeeRepository (list, search, filter, paginate)
10. **test:** add indexes, verify pagination response time <300ms on 10k rows
11. **api:** Salary history endpoints
12. **services:** SalaryHistoryService, tracking changes
13. **insights:** Insights service (stats, distribution, outliers—TDD with fixtures)
14. **api:** Insights endpoints

### Phase 3: Seeding & Scale (Day 1 late)
15. **seed:** seed_employees.py, 10k deterministic employees, batch insert
16. **test:** timing test for seed + insights query on seeded data
17. **docs:** performance.md with measured numbers

### Phase 4: Frontend (Day 2 early)
18. **frontend:** Vite scaffold, React Router, TanStack Query setup
19. **components:** EmployeeTable (pagination, search, filter, sort)
20. **components:** EmployeeForm (CRUD modal)
21. **components:** EmployeeDetail (with salary history)
22. **pages:** EmployeesPage (tie it together)
23. **tests:** table, form, detail component tests (Vitest + RTL)

### Phase 5: Insights & Polish (Day 2)
24. **components:** InsightsDashboard (KPI cards, charts with Recharts)
25. **components:** Filters for dashboard
26. **pages:** InsightsPage
27. **frontend tests:** dashboard rendering, data mocking
28. **styling:** Tailwind, responsive design, light/dark theme

### Phase 6: Deployment & Docs (Day 2 late)
29. **docker:** Dockerfile (multi-stage: build frontend, serve with FastAPI)
30. **github:** push to GitHub, CI green
31. **deploy:** Render/Railway setup, Postgres, run seed in prod, verify
32. **docs:** ai-workflow.md, tradeoffs.md, polish README with live URL + video instructions
33. **video:** Record 2-3 min demo (requirements → seeded list → search → edit with history → insights → tests → AI workflow)
34. **email:** Reply with repo link, live URL, video link

---

## Testing Strategy

### Backend Tests
- **Scope:** pytest on in-memory SQLite (fast, deterministic)
- **Unit tests:** domain models, validation, currency conversion (no DB)
- **Service tests:** business logic with fixtures (hand-computed expected values)
- **API tests:** FastAPI TestClient on full stack (but in-memory DB)
- **Target:** ≥90% coverage on domain/ and services/
- **Markers:** `@pytest.mark.slow` for seed + insights on 10k rows (run separately)
- **No sleeps, no network, no external calls**

### Frontend Tests
- **Vitest + React Testing Library**
- **Unit:** component rendering with mocked API (TanStack Query mock)
- **Integration:** table pagination, form submission (userEvent), filter bar
- **Target:** key user flows, not full coverage (UI is secondary)

---

## Quality Checklist (Before Deploy)

- [ ] `git log --oneline` shows 40-50 commits, test-first pattern visible
- [ ] `pytest -q` passes in <10 s (>90% coverage on domain/ and services/)
- [ ] `ruff check .`, `mypy .`, `black --check .` all pass
- [ ] Frontend: `npm run lint` and `npm run typecheck` pass
- [ ] `python -m app.seed` produces 10k rows in <5 s; re-run is idempotent
- [ ] Local testing: full flow works end-to-end (create, list, search, edit, insights)
- [ ] Performance verified: list <300 ms, insights <500 ms on 10k rows
- [ ] Deployed to live URL with seeded data and Postgres
- [ ] All documentation committed: requirements.md, architecture.md, tradeoffs.md, ai-workflow.md, performance.md
- [ ] README with setup, test, deploy, and links to live system

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Scope creep | Prioritize: employee list/search, insights dashboard. Cut CSV import, Playwright tests if time tight. |
| TDD discipline wavering | Commit after each test; review git log. Small commits force this. |
| Deployment cold starts | Note in README; warm the app before reviewer opens. Use Render's always-on if budget allows. |
| SQLite vs Postgres drift | Stick to standard SQL; no SQLite-specific features. Consider GitHub Actions with Postgres service if time. |
| Complex insights queries | Compute in Python first (simpler, debuggable); optimize to SQL only if needed. |
| Frontend complexity | Use shadcn/ui or MUI for components; Recharts for charts. No custom SVG/Canvas. |

---

## Technology & Architecture Decisions

- **Backend:** FastAPI with SQLAlchemy 2.x, Pydantic v2 (modern, async-capable Python stack)
- **Frontend:** React + TypeScript + Vite (fast build, strong typing)
- **Deployment:** Single Docker image (simplified ops, shared codebase)
- **Database:** Portable SQL, tested on SQLite (dev) and Postgres (prod)
- **Testing:** pytest + Vitest, comprehensive coverage, no external dependencies
- **Component library:** MUI for rapid UI development
- **Authentication:** Not required for MVP (single HR persona); flagged as first enhancement

---

## Engineering Quality Markers

1. **Product thinking first:** Requirements doc committed before code; explicit scoping and "deliberately left out" reasoning
2. **Software craftsmanship:** TDD discipline visible in commits, clean layered architecture, ≥90% test coverage
3. **Scale-aware design:** Handles 10k rows with indexes, pagination, and optimized queries; performance measured and benchmarked
4. **AI workflow documented:** CLAUDE.md, AGENTS.md, and docs/ai-workflow.md show collaborative development process
5. **Trade-off transparency:** Documented decisions and alternatives in architecture and tradeoffs docs
6. **Production-ready:** Deployed live system with seeded data; end-to-end thinking from design to deployment
7. **Clear communication:** Readable commit history, comprehensive documentation, professional code standards

---

## Implementation Timeline

1. ✅ Plan finalized and documented
2. ✅ Repository initialized with foundational docs
3. → Requirements document (1 page, product framing)
4. → Backend scaffolding with first passing test
5. → Domain models, CRUD, list/search/filter/pagination
6. → Salary history and insights engine
7. → Seed script and performance verification
8. → Frontend (table, form, dashboard)
9. → Testing and polish
10. → Deployment and documentation
11. → Demo recording and final verification
