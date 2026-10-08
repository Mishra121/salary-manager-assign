import { useState, useEffect } from 'react';
import { useListEmployees } from '../api/hooks';
import { Link } from 'react-router-dom';
import { Search, Eye } from 'lucide-react';

export default function EmployeeListPage() {
  const [page, setPage] = useState(0);
  const limit = 50;
  const [filters, setFilters] = useState({
    country: '',
    department: '',
    job_title: '',
    search: '',
  });
  const [debouncedFilters, setDebouncedFilters] = useState(filters);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedFilters(filters);
      setPage(0);
    }, 300);
    return () => clearTimeout(timer);
  }, [filters]);

  const { data, isLoading, error } = useListEmployees(page * limit, limit, debouncedFilters);

  const handleFilterChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFilters((prev) => ({ ...prev, [name]: value }));
  };

  if (isLoading) return <div className="loading" />;
  if (error) return <div className="error">Error loading employees</div>;

  const totalPages = data ? Math.ceil(data.total / limit) : 0;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Employees</h1>
        <p className="page-subtitle">Manage and view all employees in the organization</p>
      </div>

      {/* Filters */}
      <div className="filter-section">
        <div className="filter-grid">
          <div className="form-group">
            <label className="form-label">Search</label>
            <div style={{ position: 'relative' }}>
              <Search
                size={18}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  color: '#94a3b8',
                }}
              />
              <input
                type="text"
                name="search"
                placeholder="Name or email..."
                value={filters.search}
                onChange={handleFilterChange}
                className="form-input"
              />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Country</label>
            <input
              type="text"
              name="country"
              placeholder="e.g., US"
              value={filters.country}
              onChange={handleFilterChange}
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Department</label>
            <input
              type="text"
              name="department"
              placeholder="e.g., Engineering"
              value={filters.department}
              onChange={handleFilterChange}
              className="form-input"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Job Title</label>
            <input
              type="text"
              name="job_title"
              placeholder="e.g., Engineer"
              value={filters.job_title}
              onChange={handleFilterChange}
              className="form-input"
            />
          </div>
        </div>
      </div>

      {/* Summary */}
      <div style={{ marginBottom: '24px', fontSize: '14px', color: '#64748b', fontWeight: '500' }}>
        Showing <strong>{data?.total || 0}</strong> employees
      </div>

      {/* Table */}
      <div className="table-container">
        <table className="table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Job Title</th>
              <th>Department</th>
              <th>Country</th>
              <th>Salary</th>
              <th style={{ textAlign: 'center' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {data?.employees.map((emp) => (
              <tr key={emp.id}>
                <td>
                  <strong>{emp.name}</strong>
                </td>
                <td>{emp.email}</td>
                <td>{emp.job_title}</td>
                <td>{emp.department}</td>
                <td>
                  <span className="badge badge-secondary">{emp.country}</span>
                </td>
                <td>
                  <strong>
                    {emp.salary.toLocaleString('en-US', {
                      style: 'currency',
                      currency: emp.currency,
                      maximumFractionDigits: 0,
                    })}
                  </strong>
                </td>
                <td style={{ textAlign: 'center' }}>
                  <Link
                    to={`/employees/${emp.id}`}
                    className="btn btn-primary"
                    style={{ fontSize: '12px', padding: '8px 12px' }}
                  >
                    <Eye size={16} />
                    View
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <div className="pagination">
        <div className="pagination-info">
          Showing {(page * limit) + 1} - {Math.min((page + 1) * limit, data?.total || 0)} of{' '}
          {data?.total} employees
        </div>
        <div className="pagination-controls">
          <button
            onClick={() => setPage((p) => Math.max(0, p - 1))}
            disabled={page === 0}
            className="pagination-btn"
          >
            ← Previous
          </button>
          <span className="pagination-page">
            Page {page + 1} of {Math.max(1, totalPages)}
          </span>
          <button
            onClick={() => setPage((p) => p + 1)}
            disabled={page >= totalPages - 1}
            className="pagination-btn"
          >
            Next →
          </button>
        </div>
      </div>
    </div>
  );
}
