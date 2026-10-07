# Claude Development Instructions

This file documents how Claude AI was instructed to assist during development of the Salary Management System. Use this as context for understanding the code and approach.

## 🎯 Development Principles

### 1. Test-Driven Development (TDD)
- **Always write tests before implementation**
- Test structure: fail → implement → pass → refactor
- Each git commit should be atomic and aligned with this cycle
- Tests are the safety net and documentation

### 2. Code Quality > Speed
- Production-quality code, not "works locally"
- Clean, readable code that team members can understand
- Meaningful variable names, docstrings, type hints
- No shortcuts or "tech debt" comments

### 3. Small, Focused Commits
- Each commit should represent one logical change
- ~30-50 commits total for this project (not fewer, not too many)
- Commit message format: `<type>(<scope>): <subject>`
  - Types: `chore`, `docs`, `test`, `feat`, `refactor`, `perf`, `fix`
  - Example: `feat(api): add employee list with pagination`

### 4. Layered Architecture
- Router → Service → Repository → Domain
- Business logic in Service/Domain layers, easily unit testable
- HTTP handling isolated in routers
- Database queries isolated in repositories

### 5. Portable SQL
- Write SQL that works on both SQLite (dev) and Postgres (prod)
- Use SQLAlchemy ORM, not raw SQL where possible
- Parameterized queries always
- Test critical queries on both databases

### 6. Documentation First
- Requirements doc before code
- Architecture doc before major changes
- Comments explain "why," not "what"
- Commit messages tell the story

---

## 🛠️ Specific Patterns to Use

### Backend (FastAPI + SQLAlchemy)

**Models (domain/):**
```python
from pydantic import BaseModel, field_validator
from datetime import datetime
from decimal import Decimal

class EmployeeCreateRequest(BaseModel):
    name: str
    email: str
    salary: Decimal  # Always Decimal, not float
    country: str
    
    @field_validator('salary')
    @classmethod
    def validate_salary(cls, v):
        if v <= 0:
            raise ValueError('Salary must be positive')
        return v
```

**Repositories:**
```python
# Pure query logic, no business decisions
def list_employees(db: Session, skip: int = 0, limit: int = 50):
    return db.query(EmployeeModel).offset(skip).limit(limit).all()

def get_by_email(db: Session, email: str):
    return db.query(EmployeeModel).filter(EmployeeModel.email == email).first()
```

**Services:**
```python
# Business logic, calls repositories
def create_employee(db: Session, req: EmployeeCreateRequest):
    if repo.get_by_email(db, req.email):
        raise ValueError('Email already exists')
    emp = EmployeeModel(...)
    db.add(emp)
    db.commit()
    return emp
```

**API Routes:**
```python
# Thin wrappers, delegate to services
@router.post("/employees")
def create_employee(req: EmployeeCreateRequest, db: Session = Depends(get_db)):
    try:
        emp = service.create_employee(db, req)
        return emp
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Frontend (React + TS)

**API Client (typed):**
```typescript
interface Employee {
  id: number;
  name: string;
  email: string;
  salary: number;
}

const api = {
  async listEmployees(page: number, limit: number): Promise<Employee[]> {
    const res = await fetch(`/api/v1/employees?skip=${(page-1)*limit}&limit=${limit}`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  }
};
```

**TanStack Query Hook:**
```typescript
function useEmployees(page: number, limit: number) {
  return useQuery({
    queryKey: ['employees', page, limit],
    queryFn: () => api.listEmployees(page, limit),
  });
}
```

**Component (with error handling):**
```typescript
export function EmployeeTable() {
  const { data, isLoading, error } = useEmployees(1, 50);
  
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return <table>{/* render data */}</table>;
}
```

### Testing

**Backend (pytest):**
```python
def test_create_employee_with_valid_data(db_session):
    req = EmployeeCreateRequest(
        name="Alice", email="alice@example.com", 
        salary=50000, country="US"
    )
    emp = service.create_employee(db_session, req)
    assert emp.name == "Alice"
    assert emp.email == "alice@example.com"

def test_create_employee_rejects_duplicate_email(db_session):
    # Create first employee
    service.create_employee(db_session, EmployeeCreateRequest(...))
    
    # Attempt duplicate
    with pytest.raises(ValueError, match="Email already exists"):
        service.create_employee(db_session, EmployeeCreateRequest(...))
```

**Frontend (Vitest + RTL):**
```typescript
describe('EmployeeForm', () => {
  it('submits valid employee data', async () => {
    render(<EmployeeForm onSubmit={mockSubmit} />);
    
    userEvent.type(screen.getByLabelText('Name'), 'Alice');
    userEvent.type(screen.getByLabelText('Email'), 'alice@example.com');
    userEvent.type(screen.getByLabelText('Salary'), '50000');
    
    userEvent.click(screen.getByText('Create'));
    
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith(expectedData);
    });
  });
});
```

---

## 🚀 When to Ask for Help

Claude (the AI model used during development) should be asked for help with:
- ✅ Scaffolding CRUD endpoints following the pattern
- ✅ Writing test fixtures and builders
- ✅ Generating React components (table, form, dashboard)
- ✅ SQL query optimization
- ✅ Debugging test failures
- ✅ Documentation and README sections
- ✅ Code cleanup and refactoring suggestions
- ✅ Explaining architectural decisions

Claude should **not** replace human judgment on:
- ❌ Product requirements (what to build)
- ❌ Architecture decisions (layered, microservices, etc.)
- ❌ Business logic (validation rules, pricing, etc.)
- ❌ Security choices (auth, RBAC, encryption)
- ❌ Deployment strategy
- ❌ Performance trade-offs

---

## 📋 Checklist Before Each Commit

- [ ] Tests written first, failing, then passing
- [ ] Code passes `ruff check`, `mypy`, `eslint`, `tsc`
- [ ] Changes are focused and atomic
- [ ] Commit message is clear and follows convention
- [ ] Related documentation updated (if applicable)
- [ ] No commented-out code left behind
- [ ] Type hints on all public functions
- [ ] Docstrings on classes and complex functions

---

**Last Updated:** Oct 7, 2026  
**Engineer:** Vibhu Mishra
