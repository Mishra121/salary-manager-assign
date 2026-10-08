# Salary Management System - Frontend

React 18 + TypeScript + Vite-based frontend for the salary management application. Professional UI for employee management and compensation analytics.

## Setup

### Prerequisites
- Node.js 18+ and npm

### Installation

```bash
npm install
```

## Running

### Using Make Commands (Recommended)

```bash
# From project root
make frontend-start     # Start dev server on port 5173
make kill-servers       # Stop all running services
```

### Manual Development Server

```bash
npm run dev
```

Frontend starts at `http://localhost:5173`

### Production Build

```bash
npm run build
npm run preview  # Preview production build locally
```

## Project Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── client.ts           # Fetch client with error handling
│   │   ├── hooks.ts            # TanStack Query hooks
│   │   ├── types.ts            # TypeScript API types
│   │   └── __tests__/          # API tests
│   ├── components/
│   │   └── Navbar.tsx          # Navigation bar
│   ├── pages/
│   │   ├── EmployeeListPage.tsx        # Employee directory with filters
│   │   ├── EmployeeDetailPage.tsx      # Employee detail view
│   │   ├── EmployeeEditPage.tsx        # Edit employee form
│   │   ├── CreateEmployeePage.tsx      # Create employee form
│   │   └── InsightsDashboardPage.tsx   # Analytics dashboard
│   ├── App.tsx                 # Main app component with routes
│   ├── App.css                 # Professional styling (450+ lines)
│   ├── main.tsx                # Entry point
│   └── index.css               # Global styles
├── public/
│   └── favicon.svg             # App icon
├── package.json                # Dependencies
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite configuration
└── README.md                   # This file
```

## Features

### Pages
- **Employee List**: 10,000+ employees with pagination, search, and filtering
- **Employee Detail**: Full employee info + salary history timeline
- **Employee Edit**: Update employee details with validation
- **Create Employee**: Add new employee with form validation
- **Insights Dashboard**: Analytics with KPIs, charts, and outlier detection

### Technical Features
- ✅ **Type-safe API hooks** using TanStack Query (React Query)
- ✅ **Responsive design** - works on desktop, tablet, mobile
- ✅ **Professional styling** - navy and blue color scheme with proper spacing
- ✅ **Client-side validation** - email, salary, required fields
- ✅ **Multi-currency support** - automatic USD conversion
- ✅ **Debounced search** - 300ms delay prevents excessive API calls
- ✅ **Interactive charts** - Recharts for salary distribution, salary by country/department
- ✅ **Error handling** - User-friendly error messages
- ✅ **Loading states** - Proper feedback during data fetching

## API Integration

### Environment

The frontend proxies API requests to the backend:

```typescript
// During development: http://localhost:8000/api
// In production: configured via environment
```

See `vite.config.ts` for proxy configuration.

### API Hooks

```typescript
// Employee operations
useEmployees(page, limit, filters)
useEmployeeDetail(id)
useCreateEmployee()
useUpdateEmployee(id)
useDeleteEmployee(id)

// Insights/Analytics
useInsights()

// Salary history
useSalaryHistory(employeeId)
useUpdateSalary(employeeId)
```

All hooks are fully typed with TypeScript.

## Code Quality

### Linting & Formatting

```bash
# Check code quality
npm run lint

# Format code
npm run format
```

### Type Checking

```bash
# Check TypeScript
npx tsc --noEmit
```

## Testing

### Unit Tests

```bash
npm run test
```

### Build Verification

```bash
npm run build
```

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Styling

The frontend uses a custom CSS stylesheet (450+ lines) with:
- **Color scheme**: Navy (#0f172a) and blue (#2563eb) primary, with complementary accent colors
- **Responsive grids**: CSS Grid for layouts that adapt to screen size
- **Professional components**: Cards, tables, forms, badges, and buttons
- **Consistent spacing**: 8px/16px/32px rhythm throughout
- **Hover effects**: Subtle interactions for better UX
- **Dark backgrounds**: Modern design with proper contrast

## Performance

- **Bundle size**: Optimized with Vite tree-shaking
- **Code splitting**: Automatic per-route splitting
- **Lazy loading**: Images and components load on demand
- **Query caching**: TanStack Query prevents unnecessary API calls
- **Pagination**: Server-side pagination for 10k+ employee lists

## Troubleshooting

### "Cannot find module" errors
```bash
npm install
npm run build
```

### Port 5173 already in use
```bash
# Kill the process
make kill-servers

# Or manually specify different port
npm run dev -- --port 3000
```

### API connection errors
- Ensure backend is running on port 8000
- Check browser console for network errors
- Verify proxy configuration in `vite.config.ts`

## Development Tips

1. **HMR (Hot Module Replacement)** is enabled - changes save instantly
2. **Use React DevTools** browser extension for component inspection
3. **Check Network tab** in DevTools to monitor API calls
4. **Use TypeScript** - let the compiler catch errors early
5. **Follow component patterns** - see existing pages for consistency

## Architecture

### Component Hierarchy
```
App (Router)
├── Navbar
└── Routes
    ├── EmployeeListPage
    ├── EmployeeDetailPage
    ├── EmployeeEditPage
    ├── CreateEmployeePage
    └── InsightsDashboardPage
```

### State Management
- **React hooks** for local component state
- **TanStack Query** for server state (API data)
- **URL state** for pagination and filters

### API Pattern
```typescript
// Define hook
const useEmployees = (page: number) => {
  return useQuery({
    queryKey: ['employees', page],
    queryFn: () => api.listEmployees(page),
  });
};

// Use in component
const { data, isLoading, error } = useEmployees(1);
```

## Related Documentation

- [Backend API](../backend/README.md) - FastAPI server
- [Architecture](../docs/architecture.md) - System design
- [Requirements](../docs/requirements.md) - Feature scope
- [Trade-offs](../docs/tradeoffs.md) - Design decisions
