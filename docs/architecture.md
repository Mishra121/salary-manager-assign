# Architecture: Salary Management System

## System Overview

The Salary Management System is a full-stack web application designed to handle employee salary data and compensation analytics at scale (10,000+ employees).

```
┌─────────────────────────────────────────────────────────────────┐
│                       Frontend (React + Vite)                   │
│  ┌───────────────┬──────────────┬──────────────────────────┐   │
│  │ Employee List │ Create/Edit  │ Salary History + Insights│   │
│  │ (Table +      │ (Form)       │ (Charts + KPIs)          │   │
│  │  Pagination)  │              │                          │   │
│  └───────────────┴──────────────┴──────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ (HTTP REST API)
                           ↓
┌─────────────────────────────────────────────────────────────────┐
│              Backend (FastAPI + SQLAlchemy)                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ API Router Layer (HTTP endpoints)                      │    │
│  │  ├─ /employees (CRUD)                                 │    │
│  │  ├─ /employees/{id}/salary-history                    │    │
│  │  └─ /insights (analytics)                             │    │
│  └────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Service Layer (Business Logic)                         │    │
│  │  ├─ EmployeeService (CRUD logic)                      │    │
│  │  ├─ SalaryHistoryService (tracking)                   │    │
│  │  └─ InsightsService (analytics)                       │    │
│  └────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Repository Layer (Data Access)                         │    │
│  │  ├─ EmployeeRepository (queries, filters)             │    │
│  │  ├─ SalaryHistoryRepository (immutable records)       │    │
│  │  └─ InsightsRepository (aggregations)                 │    │
│  └────────────────────────────────────────────────────────┘    │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ Domain Layer (Pure Business Rules)                     │    │
│  │  ├─ Employee (model + validation)                     │    │
│  │  ├─ EmploymentType, EmployeeStatus (enums)            │    │
│  │  └─ CurrencyConverter (FX logic)                       │    │
│  └────────────────────────────────────────────────────────┘    │
└─────────────────┬──────────────────────────────────────────────┘
                  │ (SQLAlchemy ORM)
                  ↓
        ┌─────────────────────────────┐
        │  Database (SQLite / Postgres)│
        │  ├─ employees               │
        │  ├─ salary_history          │
        │  └─ (see DB Schema)         │
        └─────────────────────────────┘
```

---

## Database Schema

### `employees` table
Stores current employee information.

```sql
CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL INDEX,
    email VARCHAR(255) UNIQUE NOT NULL INDEX,
    job_title VARCHAR(255) NOT NULL INDEX,
    department VARCHAR(255) NOT NULL INDEX,
    country VARCHAR(3) NOT NULL INDEX,  -- ISO 3166-1 alpha-2
    employment_type ENUM NOT NULL,      -- FULL_TIME, PART_TIME, CONTRACT
    hire_date DATE NOT NULL,
    salary NUMERIC(12, 2) NOT NULL,     -- Always Decimal for precision
    currency VARCHAR(3) NOT NULL,       -- ISO 4217 (USD, EUR, GBP, etc)
    status ENUM NOT NULL,               -- ACTIVE, INACTIVE, ON_LEAVE
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CHECK (salary > 0),
    UNIQUE (email),
    
    -- Indexes for fast filtering/aggregation
    INDEX idx_employees_country (country),
    INDEX idx_employees_department (department),
    INDEX idx_employees_job_title (job_title),
    INDEX idx_employees_country_department_title (country, department, job_title)
);
```

**Why Numeric(12, 2)?**
- Stores exact decimal values (no float precision errors)
- Supports salaries up to 9,999,999,999.99
- Decimal places fixed at 2 (cents)
- Critical for financial accuracy

---

### `salary_history` table
Immutable audit trail of all salary changes.

```sql
CREATE TABLE salary_history (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL INDEX,
    old_salary NUMERIC(12, 2) NULL,     -- NULL for initial hire
    new_salary NUMERIC(12, 2) NOT NULL, -- Required
    currency VARCHAR(3) NOT NULL,       -- Captured at time of change
    effective_date DATE NOT NULL INDEX,
    reason VARCHAR(255) NULL,           -- "Annual raise", "Promotion", etc
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Constraints
    CHECK (new_salary > 0),
    INDEX idx_salary_history_employee (employee_id),
    INDEX idx_salary_history_employee_effective_date (employee_id, effective_date),
    
    -- Foreign key to employees (soft constraint, not enforced in SQLite)
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
```

**Why Immutable?**
- Audit trail: all changes preserved forever
- No updates or deletes allowed
- Supports salary progression analysis
- Enables compliance reporting

---

## Technology Stack

### Backend
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | FastAPI | Modern, async, built-in validation (Pydantic) |
| **ORM** | SQLAlchemy 2.x | Portable SQL, no lock-in, mature ecosystem |
| **Database (Dev)** | SQLite | Zero setup, fast for 10k rows, perfect for local testing |
| **Database (Prod)** | Postgres | JSONB, window functions, proven at scale |
| **Testing** | pytest | Fast, fixtures, parametrization, great assertion messages |
| **Linting** | ruff | 10-100x faster than flake8, written in Rust |
| **Type Checking** | mypy | Catches type errors before runtime |
| **ASGI Server** | uvicorn | Production-ready, used by FastAPI guide |
| **Package Manager** | uv | 10-20x faster than pip, written in Rust |

### Frontend *(Step 4)*
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Framework** | React 18 + TypeScript | Type-safe, component reusability, large ecosystem |
| **Build Tool** | Vite | 10-100x faster than Webpack for dev, ESM-first |
| **Styling** | shadcn/ui or MUI | Pre-built components, accessibility built-in |
| **Data Fetching** | TanStack Query | Caching, background sync, automatic refetch logic |
| **Tables** | TanStack Table (v8) | Headless, pagination, sorting, filtering at 10k rows |
| **Charts** | Recharts | React-native, responsive, simple API |
| **Testing** | Vitest + RTL | Jest-compatible, Vite-native, fast |

### Deployment
| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Container** | Docker | Single image, reproducible across machines |
| **Multi-Stage** | Yes | Separate build stage (Node/Python) → runtime stage (minimal) |
| **Platform** | Render or Railway | Free tier, Postgres included, easy GitHub integration |
| **CI/CD** | GitHub Actions | Free with repo, no vendor lock-in |

---

## Layered Architecture

### 1. **Domain Layer** (`app/domain/`)
Pure business logic, no framework dependencies. Easily unit-testable.

```python
# Example: Employee domain model
class Employee:
    name: str
    email: str
    salary: Decimal  # Always Decimal for precision
    country: str
    
    def __post_init__(self):
        # Validation happens here
        if self.salary <= 0:
            raise ValueError("Salary must be positive")
        if len(self.country) != 2:
            raise ValueError("Country must be ISO 3166-1 alpha-2")
```

**Benefits:**
- Can be tested without database or HTTP framework
- Can be reused in CLI, batch jobs, webhooks
- Validation is testable in isolation
- No mock complexity

### 2. **Repository Layer** (`app/repositories/`)
Data access only. Queries and persistence, no business logic.

```python
class EmployeeRepository:
    def list(self, skip: int, limit: int, country: str = None):
        # Pure SQL/ORM query logic
        query = db.query(EmployeeModel)
        if country:
            query = query.filter(EmployeeModel.country == country)
        return query.offset(skip).limit(limit).all()
    
    def get_by_email(self, email: str):
        # Returns ORM model or None
        return db.query(EmployeeModel).filter_by(email=email).first()
```

**Benefits:**
- Testable with in-memory SQLite
- Easy to swap implementations (e.g., add Redis cache)
- SQL is isolated and reviewable
- Indexes documented in one place

### 3. **Service Layer** (`app/services/`)
Business logic, coordinates repositories and domain models.

```python
class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo
    
    def create_employee(self, request: EmployeeCreateRequest) -> Employee:
        # Check for duplicates
        if self.repo.get_by_email(request.email):
            raise ValueError("Email already exists")
        
        # Create domain model (validates)
        employee = Employee(**request.dict())
        
        # Persist
        model = EmployeeModel.from_domain(employee)
        return self.repo.create(model)
```

**Benefits:**
- All business rules in one place
- Easy to test with mock repositories
- HTTP layer doesn't touch repositories directly
- Reusable across HTTP/CLI/batch jobs

### 4. **Router Layer** (`app/api/`)
HTTP endpoints only. Delegates to services, handles HTTP semantics.

```python
@router.post("/employees", response_model=EmployeeResponse)
def create_employee(
    request: EmployeeCreateRequest,
    db: Session = Depends(get_db),
    service: EmployeeService = Depends(get_employee_service),
):
    try:
        emp = service.create_employee(request)
        return EmployeeResponse.from_domain(emp)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Benefits:**
- Thin wrapper, easy to audit
- HTTP error handling in one place
- Can change HTTP library without touching business logic
- Dependency injection makes testing easy

---

## Key Design Decisions

### 1. **Immutable Salary History**
- Every salary change creates a new record
- No updates or deletes allowed
- Foreign key from `salary_history.employee_id` to `employees.id` (soft constraint on SQLite)
- Composite index on `(employee_id, effective_date)` for fast timeline queries

### 2. **Decimal for Money**
- All salaries stored as `Numeric(12, 2)` in database
- Python: `Decimal` type (never `float`)
- Prevents rounding errors in aggregations
- Precision preserved through currency conversion

### 3. **Currency Conversion (Static Rates)**
- Rates updated quarterly, not live
- One-time lookup in `CurrencyConverter` domain service
- All analytics aggregated in USD
- Decouples system from external FX APIs

### 4. **Indexes for Scale**
- Single-column on `country`, `department`, `job_title` for fast filters
- Composite on `(country, department, job_title)` for complex filters
- On `effective_date` for salary history timeline queries
- Reduces analytics queries from seconds to milliseconds at 10k rows

### 5. **Server-Side Pagination**
- Prevents loading all 10k rows into memory
- Frontend requests `?skip=0&limit=50`
- Backend returns `{total, skip, limit, employees: [...]}`
- Enables browsing 10k rows without lag

---

## Data Flow Examples

### Employee Creation
```
POST /api/v1/employees
├─ Router receives EmployeeCreateRequest (validated by Pydantic)
├─ Calls EmployeeService.create_employee()
│  ├─ Calls EmployeeRepository.get_by_email() → checks duplicate
│  ├─ Creates Employee domain model (validation runs here)
│  ├─ Converts to EmployeeModel (ORM)
│  └─ Calls EmployeeRepository.create() → SQL INSERT
├─ Converts result to EmployeeResponse (JSON)
└─ Returns HTTP 201 Created
```

### Salary Update + History
```
PUT /api/v1/employees/{id}
├─ Update employee.salary = new_amount
├─ Create SalaryHistoryModel(old_salary, new_salary, effective_date, reason)
├─ INSERT into salary_history (immutable record)
├─ UPDATE employees.salary (current value)
└─ Returns updated employee with new salary
```

### Insights Query
```
GET /api/v1/insights
├─ InsightsRepository.get_headline_kpis()
│  ├─ COUNT(*) as headcount
│  ├─ SUM(salary * fx_rate) as total_payroll_usd
│  ├─ AVG(salary * fx_rate) as avg_salary_usd
│  ├─ PERCENTILE_CONT(salary * fx_rate) as median_salary_usd
│  └─ (Postgres) or (Python fallback for SQLite)
├─ InsightsRepository.get_salary_by_country()
│  └─ GROUP BY country, with stats per group
├─ InsightsRepository.get_salary_distribution()
│  └─ Bucket salaries (0-50k, 50-100k, ...) with counts
└─ Returns InsightsResponse (all aggregates in one call)
```

---

## Performance Targets & Strategies

| Operation | Target | Strategy |
|-----------|--------|----------|
| **List 10k employees** | <300 ms | Index on (country, department), offset/limit pagination |
| **Search by name** | <300 ms | Full-text index or `LIKE` with index prefix |
| **Insights (headcount, avg, median)** | <500 ms | SQL aggregation, single query, window functions on Postgres |
| **Salary history timeline** | <100 ms | Index on `(employee_id, effective_date)` for range scan |
| **Outlier detection** | <500 ms | GROUP BY job_title, compute stddev, then filter |
| **Seed 10k employees** | <5 sec | Batch insert (500 at a time), pre-generated seed data |

---

## Scalability Considerations

### Current: 10,000 Employees
- SQLite sufficient for dev/testing
- Postgres required for production
- All queries index-backed, sub-second response times

### If 100,000 Employees (Future)
- Batch pagination already in place (trivial)
- Partitioning by country (optional)
- Archive old salary history (keep 5 years, archive older)
- Materialized views for insights (refresh nightly)

### If Real-Time Analytics Needed
- Add Redis cache on top of DB queries
- TanStack Query on frontend caches for 5 min
- Database replication for read-heavy insights

---

## Testing Strategy

| Layer | Tool | Coverage | Example |
|-------|------|----------|---------|
| **Domain** | pytest | 95%+ | Employee validation, currency conversion |
| **Repository** | pytest + SQLite | 90%+ | Queries, filters, edge cases (no employees, pagination boundaries) |
| **Service** | pytest + mocks | 90%+ | Business logic, error handling, duplicate detection |
| **Router** | pytest + TestClient | 80%+ | HTTP status codes, request/response format, error messages |
| **Frontend** | Vitest + RTL | 70%+ | Form validation, list rendering, chart data |
| **E2E** | (Optional) | 5-10% | Critical path (create employee, view salary, see on dashboard) |

**Note:** We prioritize unit tests (domain + services) over E2E, trading breadth for speed and maintainability.

---

## Deployment Architecture

```
GitHub Repository
    ↓
GitHub Actions (CI)
    ├─ Lint (ruff, mypy, eslint, tsc)
    ├─ Tests (pytest, vitest)
    └─ Build Docker image
           ↓
       Docker Registry (GitHub Packages or DockerHub)
           ↓
Render / Railway (PaaS)
    ├─ Pull Docker image
    ├─ Attach Postgres managed database
    ├─ Set environment variables (DATABASE_URL, etc)
    ├─ Start container (uvicorn on port 8000)
    └─ Serve frontend static files from FastAPI
           ↓
      Public URL (e.g., app.render.com)
```

### Dockerfile (Multi-Stage)
```dockerfile
# Stage 1: Build frontend
FROM node:18 AS frontend-build
WORKDIR /app/frontend
COPY frontend/package*.json .
RUN npm ci
COPY frontend/ .
RUN npm run build  # Outputs to dist/

# Stage 2: Build backend
FROM python:3.11-slim
WORKDIR /app

# Copy frontend dist into backend static folder
COPY --from=frontend-build /app/frontend/dist /app/static

# Install Python dependencies
COPY backend/pyproject.toml backend/uv.lock .
RUN pip install uv && uv sync --no-dev

# Copy backend code
COPY backend/app ./app

# Expose port
EXPOSE 8000

# Start server (FastAPI serves static + API)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Monitoring & Observability (Future)

When deployed, consider adding:
- **Logs:** Structured JSON logs to stdout (CloudWatch/Datadog)
- **Metrics:** Prometheus endpoint for query latency, error rates
- **Alerts:** PagerDuty for database connection errors, high query latency
- **Tracing:** OpenTelemetry for slow request debugging

For MVP, logging to stdout is sufficient; platform (Render/Railway) captures and makes searchable.

---

**Last Updated:** October 8, 2026  
**Author:** Vibhu Mishra  
**Status:** Complete for Backend (Frontend docs coming Step 4)
