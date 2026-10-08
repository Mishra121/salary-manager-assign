# Trade-offs: Salary Management System

This document captures key architectural and product decisions, their rationale, and alternatives considered.

---

## 1. **SQLite (Dev) vs Postgres (Prod)**

### Decision
- **Development:** SQLite (zero setup, file-based)
- **Production:** Postgres (proven at scale)

### Rationale
- SQLite is perfect for local dev and testing (everything in one file, no Docker needed)
- Postgres required for prod (better concurrency, window functions, JSONB if we add it later)
- Switching is trivial: just change `DATABASE_URL` in config

### Trade-offs
| Pro | Con |
|-----|-----|
| Dev is fast (no DB setup) | SQLite has differences (e.g., window functions are Python-computed) |
| Same ORM (SQLAlchemy) on both | Need to test on both for complete coverage (not fully done yet) |
| Portable (test file is in git if needed) | Window functions (e.g., ROW_NUMBER) only on Postgres |

### Alternative Considered
- **Always use Postgres:** Docker Compose would be required for all devs; slows onboarding. Not chosen because SQLite is sufficient for testing and MVP.

### Decision Status
✅ **Accepted.** Easy to test on Postgres in CI; SQL queries are portable.

---

## 2. **Decimal vs Float for Money**

### Decision
- All salaries: `Numeric(12, 2)` in DB, `Decimal` in Python
- Never `float`

### Rationale
- `float` has precision errors: `0.1 + 0.2 != 0.3` (IEEE 754)
- Financial calculations require exact decimal representation
- `Decimal` is standard for money in Python
- Database `Numeric` is exact; no rounding on retrieval

### Trade-offs
| Pro | Con |
|-----|-----|
| Mathematically correct aggregations | Slightly slower than float (negligible) |
| No surprise rounding errors | Developers must remember to use `Decimal`, not `float` |
| Compliant with financial standards | More verbose in code (explicit conversions) |

### Examples of Why This Matters
```python
# With float:
salaries_float = [50000.0, 60000.0, 70000.0]
avg = sum(salaries_float) / len(salaries_float)  # 60000.0
# But across many records, errors compound

# With Decimal (correct):
from decimal import Decimal
salaries = [Decimal("50000.00"), Decimal("60000.00"), Decimal("70000.00")]
avg = sum(salaries) / len(salaries)  # Decimal('60000.00')
```

### Alternative Considered
- **Use integers (cents):** `salary_cents: int` to store $50,000 as `5000000`. Avoids floating point entirely. Not chosen because Decimal is cleaner to work with and already exact.

### Decision Status
✅ **Accepted.** Non-negotiable for financial correctness.

---

## 3. **Immutable Salary History (No Updates/Deletes)**

### Decision
- Salary history records can only be created
- Updates and deletes are forbidden (database constraints prevent them)
- Corrections require a new record with reason

### Rationale
- Audit trail: every change is permanent and traceable
- Legal compliance: salary changes must be documented
- Prevents accidental data loss
- Makes historical analysis reliable

### Trade-offs
| Pro | Con |
|-----|-----|
| Perfect audit trail | Can't fix data entry mistakes silently |
| Enables compliance reporting | Requires discipline (document corrections as new records) |
| Data integrity guaranteed | Storage grows over time (archive old records if needed) |
| Simple to implement | UI must explain why updates create new records |

### Example
```
Mistake: Employee hired at $50k, entered as $500k
Solution: Create new record with $50k and reason "Correction: initial hire salary"
Audit trail: now shows both $500k and $50k with reasons and dates
```

### Alternative Considered
- **Allow updates:** Simpler for users, but loses audit trail. Rejected because HR/compliance needs to track who changed what and when.
- **Soft deletes:** Flag records as deleted instead of truly immutable. Not chosen because simpler model (no deletes at all) is clearer.

### Decision Status
✅ **Accepted.** Immutability is a feature for compliance, not a limitation.

---

## 4. **Static Currency Rates vs Live FX API**

### Decision
- Static exchange rates, updated quarterly by HR
- No real-time FX conversion

### Rationale
- MVP doesn't need real-time rates; salaries change slowly
- Live FX adds external dependency and latency
- Static rates are consistent for month-end reporting
- Simpler to implement and test

### Trade-offs
| Pro | Con |
|-----|-----|
| No external dependency (fast, reliable) | Rates can drift from market over quarter |
| Consistent month-end reporting | Manual update overhead (once per quarter) |
| Testable without mocking external API | Employees paid in different currencies need conversion |
| Deterministic (no random failures) | Multi-currency comparisons slightly stale |

### Exchange Rates (Q4 2026 - Example)
```python
EXCHANGE_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.50,
    "AUD": 1.53,
    "CAD": 1.36,
    "JPY": 148.50,
    "SEK": 11.25,
}
```

### Alternative Considered
- **Live FX (OpenExchange or similar):** More accurate, but adds latency (~100ms) and dependency. Could fail. Not chosen for MVP because quarterly accuracy is sufficient.
- **User-supplied rates:** Each employee's hire salary uses their hire-date rate. Too complex; requires storing rate per salary history record.

### Decision Status
✅ **Accepted.** Easy to upgrade to live FX later (CurrencyConverter is in domain layer).

---

## 5. **Server-Side Pagination vs Client-Side**

### Decision
- Server-side pagination: frontend requests `?skip=0&limit=50`
- Server returns `{total, employees: [...]}`

### Rationale
- 10,000 employees can't fit in memory / JSON response
- Scales to 100k+ without code change
- Reduces bandwidth (only send what's displayed)
- Database handles sorting and filtering before paginating

### Trade-offs
| Pro | Con |
|-----|-----|
| Handles 10k+ rows effortlessly | Slight latency on first load |
| Efficient (only load visible rows) | UI complexity (need to track offset/limit) |
| Database can optimize (filter before limit) | Can't search across all results without multiple calls |
| Standard for large datasets | No "load all" button (by design) |

### Example Flow
```
User clicks "Next" (page 2, 50/page)
Frontend: GET /api/v1/employees?skip=50&limit=50
Backend: SELECT * FROM employees LIMIT 50 OFFSET 50
Response: {total: 10000, skip: 50, limit: 50, employees: [...50 records...]}
UI renders page 2
```

### Alternative Considered
- **Client-side pagination:** Load all 10k, paginate in UI. Fast for small datasets, but 10k salaries is ~1-2 MB JSON. Rejected because wasteful and bad UX (initial load 2-3 sec).
- **Cursor-based pagination:** More complex for UI, but better for real-time data. Not chosen for MVP because offset/limit is simpler.

### Decision Status
✅ **Accepted.** Standard for enterprise apps; required for scale.

---

## 6. **TDD (Test-First) vs Test-After**

### Decision
- Tests written before implementation
- Each feature: failing test → implementation → green test → refactor

### Rationale
- Catches requirements early (test clarifies "what should it do?")
- Prevents over-engineering (tests define scope)
- Refactoring is safe (tests catch regressions)
- Tests are documentation (read test to understand feature)

### Trade-offs
| Pro | Con |
|-----|-----|
| Fewer bugs ship | Slightly slower initial development |
| Refactoring is safe | Developers must think before coding |
| Tests are up-to-date (by definition) | Some tests become obvious/redundant |
| Code review is faster (code matches tests) | Requires discipline; easy to slip into test-after |

### Example
```python
# Step 1: Write test (FAILS)
def test_create_employee_rejects_duplicate_email():
    emp1 = create_employee(email="alice@acme.com", ...)
    with pytest.raises(ValueError, match="Email already exists"):
        create_employee(email="alice@acme.com", ...)

# Step 2: Implement (PASSES test)
def create_employee(email, ...):
    if repo.get_by_email(email):
        raise ValueError("Email already exists")
    ...

# Step 3: Refactor (still PASSES)
def create_employee(request: EmployeeCreateRequest):
    if repo.get_by_email(request.email):
        raise ValueError(f"Email {request.email} already registered")
    ...
```

### Alternative Considered
- **Test-after:** Write code first, tests second. Faster initially, but tests often skip error cases. Not chosen because MVP needs high confidence.

### Decision Status
✅ **Accepted.** Every feature has failing test → passing impl → refactor cycle.

---

## 7. **Layered Architecture (Router → Service → Repository → Domain)**

### Decision
```
Router (HTTP)
  ↓
Service (Business Logic)
  ↓
Repository (Data Access)
  ↓
Domain (Pure Model + Validation)
```

### Rationale
- **Domain** layer has zero external dependencies; can be tested without mocks
- **Repository** layer is testable with in-memory SQLite; SQL logic isolated
- **Service** layer is testable with mock repositories; business rules clear
- **Router** layer is thin; just HTTP handling

### Trade-offs
| Pro | Con |
|-----|-----|
| Easy to test each layer in isolation | 4 layers can feel like overhead for small features |
| Business logic not tied to HTTP/DB | More files to navigate (domain, repo, service, router) |
| Code can be reused (CLI, batch jobs could use services) | Slight latency (more function calls) — negligible |
| Clear separation of concerns | Requires discipline (don't leak HTTP into services) |

### Example: Adding a Feature
```
Requirement: "Allow filtering employees by department"

1. Domain: Add validation (department must exist)
2. Repository: Add filter_by_department(db, dept) method
3. Service: Add list_employees_by_department(dept) method
4. Router: Add ?department=Engineering query param

Each layer has 1-2 lines; changes are isolated.
```

### Alternative Considered
- **Flat structure:** Services directly touch database and HTTP. Faster to start, but hard to refactor later. Not chosen because we want clean tests.
- **CQRS (Command Query Responsibility Segregation):** Separate read and write paths. Overkill for MVP; adds complexity.

### Decision Status
✅ **Accepted.** Clear boundaries enable fast iteration without technical debt.

---

## 8. **Single HR Persona (No Auth/RBAC)**

### Decision
- No login, no multi-user support
- Single HR Manager can view and edit all data
- Deployed on internal network (trusted environment)

### Rationale
- MVP scope: answer "how do we pay people?"
- Auth/RBAC adds 20-30% complexity
- Requirement doesn't mention multiple roles
- Can add auth in Step 2 (first production enhancement)

### Trade-offs
| Pro | Con |
|-----|-----|
| Simple, ships faster | Doesn't scale to multi-user | 
| No credential management | No audit logging (who changed what) |
| No role-based filtering | Can't restrict data (e.g., only VP salaries to execs) |
| Cleaner API surface | Not suitable for external-facing systems |

### Example: Adding Auth Later
```python
# Easy to add middleware
from fastapi_oauth import require_role

@router.get("/employees")
@require_role("hr_manager")  # New decorator
def list_employees(...):
    ...
```

### Alternative Considered
- **Shared secret token:** All requests include a secret header. Better than nothing, but false sense of security. Not chosen because internal network is sufficient.
- **RBAC from day 1:** Finance sees only salaries, HR sees all, VP sees summary. Too complex for MVP; added after feedback.

### Decision Status
✅ **Accepted.** Will be first post-launch feature; CLAUDE.md includes implementation plan.

---

## 9. **Annual Salary Only (No Bonus, Equity, Benefits)**

### Decision
- `salary` field = base annual compensation only
- Excludes: bonuses, stock options, benefits (health, 401k)
- Stored as `currency` + `amount` (multi-currency)

### Rationale
- Scope: "Salary Management System", not "Total Comp"
- Bonus varies month-to-month (can add quarterly history later)
- Equity is complex (vesting, strike price, FMV); separate system
- Benefits are role/location-specific; also separate

### Trade-offs
| Pro | Con |
|-----|-----|
| Focused scope | "Average salary" doesn't include bonuses |
| Clean data model | Pay equity analysis incomplete (missing bonus data) |
| Can be extended (add bonus history table) | Not comprehensive compensation view |
| Easy to understand for HR | Market comparisons limited (only base salary) |

### Rationale for Future
```python
# Easy to add later (new table, same pattern)
class BonusHistoryModel:
    employee_id: int
    year: int
    bonus_amount: Decimal
    effective_date: date
    reason: str  # "Annual bonus", "Sign-on bonus", etc
```

### Alternative Considered
- **Total Comp = Salary + Bonus + Stock Value:** Adds 2-3x complexity. Not chosen because bonus/equity systems are typically separate.
- **Annualized hourly:** For part-time employees, store hourly rate + hours/week. Not chosen because company likely has annual budgets.

### Decision Status
✅ **Accepted.** Scope is clear; easy to extend later.

---

## 10. **Seed 10k Employees (Deterministic)**

### Decision
- Seed script generates 10k deterministic employees
- Same seed (42) always produces same data
- Realistic: 9 countries, proper salary distributions, varied titles/departments

### Rationale
- Enables performance testing locally
- Demo has real data (not 5 fake records)
- Idempotent (can re-run; clears before inserting)
- Consistent for teaching/debugging (same data every time)

### Trade-offs
| Pro | Con |
|-----|-----|
| Performance testing possible locally | Uses ~50 MB disk (SQLite) |
| Demo looks professional | Batch insert takes ~2-3 sec (still fast) |
| Deterministic (reproducible) | Not realistic for salary distributions (simplified) |
| Can adjust `seed=` to get different data | Employees are fake (test@acme.com, same first names) |

### Alternative Considered
- **Load from CSV:** Requires CSV file, adds setup step. Not chosen because in-code generation is cleaner.
- **Procedural (random each time):** Harder to debug (data always different). Not chosen because determinism aids testing.

### Decision Status
✅ **Accepted.** Necessary for both performance validation and demo appeal.

---

## 11. **Recharts for Frontend Charts (When Ready)**

### Decision
- Use Recharts for salary distribution, insights visualizations
- (Applied in Step 4: Frontend)

### Rationale
- React-native, responsive, simple API
- Good defaults (axes, legend, tooltips)
- Lightweight (~40 KB gzipped)
- Large community, good docs

### Trade-offs
| Pro | Con |
|-----|-----|
| Works great for basic charts | Limited customization (if we need complex chart) |
| Great with Vite/React workflow | Slight overhead for static charts (D3 is smaller) |
| Responsive by default | Library lock-in (switching later is costly) |
| Good performance | Fewer sophisticated statistical charts (e.g., violin plots) |

### Example Usage
```typescript
<LineChart data={salaryByYear}>
  <CartesianGrid strokeDasharray="3 3" />
  <XAxis dataKey="year" />
  <YAxis />
  <Tooltip formatter={(value) => `$${value.toLocaleString()}`} />
  <Line type="monotone" dataKey="salary" stroke="#8884d8" />
</LineChart>
```

### Alternative Considered
- **D3.js:** Full control, smaller bundle, steeper learning curve. Not chosen because Recharts is faster to iterate.
- **Apache ECharts:** More advanced visualizations, larger bundle. Not chosen for MVP.
- **Native SVG:** No learning curve, but manual axis/legend. Not chosen because reinventing is slow.

### Decision Status
✅ **Tentatively accepted.** Will validate in Step 4 (frontend build).

---

## Summary Table

| Decision | Choice | Why | Risk | Status |
|----------|--------|-----|------|--------|
| Database (Dev/Prod) | SQLite / Postgres | Scale + simplicity | None | ✅ |
| Money Storage | Decimal | Precision | None | ✅ |
| Salary History | Immutable | Audit trail | Complexity | ✅ |
| Currency Rates | Static | Simplicity | Drift | ✅ |
| Pagination | Server-side | Scale | Latency | ✅ |
| Testing | TDD | Quality | Discipline | ✅ |
| Architecture | Layered | Testability | Overhead | ✅ |
| Auth | None (MVP) | Speed | Security* | ✅ |
| Scope | Base salary | Focus | Incompleteness | ✅ |
| Seeding | Deterministic 10k | Performance | Realism | ✅ |
| Charts | Recharts | Speed | Customization | ✅ |

*Security Risk: Deployed on internal network only; add auth in next phase.

---

**Last Updated:** October 8, 2026  
**Author:** Vibhu Mishra  
**Status:** Complete for MVP decision review
