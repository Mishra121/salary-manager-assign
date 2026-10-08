import { useState } from 'react';
import { useCreateEmployee } from '../api/hooks';
import { useNavigate, Link } from 'react-router-dom';
import { ArrowLeft, User } from 'lucide-react';

const EMPLOYMENT_TYPES = ['FULL_TIME', 'PART_TIME', 'CONTRACT'];
const COUNTRIES = ['US', 'GB', 'DE', 'FR', 'IN', 'AU', 'CA', 'JP', 'SE'];
const DEPARTMENTS = ['Engineering', 'Product', 'Sales', 'Marketing', 'HR'];

export default function CreateEmployeePage() {
  const navigate = useNavigate();
  const { mutate: createEmployee, isPending } = useCreateEmployee();

  const [formData, setFormData] = useState({
    name: '',
    email: '',
    job_title: '',
    department: '',
    country: 'US',
    employment_type: 'FULL_TIME',
    hire_date: new Date().toISOString().split('T')[0],
    salary: '',
    currency: 'USD',
  });

  const [error, setError] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    setError('');
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!formData.name || !formData.email || !formData.job_title || !formData.salary) {
      setError('Please fill in all required fields');
      return;
    }

    createEmployee(
      {
        ...formData,
        salary: parseFloat(formData.salary),
        employment_type: formData.employment_type as 'FULL_TIME' | 'PART_TIME' | 'CONTRACT',
      },
      {
        onSuccess: (employee) => {
          navigate(`/employees/${employee.id}`);
        },
        onError: (err) => {
          setError(err instanceof Error ? err.message : 'Failed to create employee');
        },
      }
    );
  };

  return (
    <div>
      <Link to="/" className="back-link">
        <ArrowLeft size={18} />
        Back to Employees
      </Link>

      <div className="max-w-2xl mx-auto">
        <div className="card">
          <div className="card-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <div style={{
                width: '48px',
                height: '48px',
                borderRadius: '8px',
                background: '#dbeafe',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
              }}>
                <User size={24} style={{ color: '#2563eb' }} />
              </div>
              <div>
                <h1 className="page-title" style={{ marginBottom: '4px' }}>
                  Create New Employee
                </h1>
                <p style={{ margin: 0, color: '#64748b', fontSize: '14px' }}>
                  Add a new employee to the system
                </p>
              </div>
            </div>
          </div>

          {error && <div className="error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '24px',
              marginTop: '24px',
            }}>
              {/* Name */}
              <div className="form-group">
                <label htmlFor="name" className="form-label">
                  Full Name *
                </label>
                <input
                  id="name"
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="John Doe"
                  required
                />
              </div>

              {/* Email */}
              <div className="form-group">
                <label htmlFor="email" className="form-label">
                  Email Address *
                </label>
                <input
                  id="email"
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="john@company.com"
                  required
                />
              </div>

              {/* Job Title */}
              <div className="form-group">
                <label htmlFor="job_title" className="form-label">
                  Job Title *
                </label>
                <input
                  id="job_title"
                  type="text"
                  name="job_title"
                  value={formData.job_title}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Senior Engineer"
                  required
                />
              </div>

              {/* Department */}
              <div className="form-group">
                <label htmlFor="department" className="form-label">
                  Department
                </label>
                <select
                  id="department"
                  name="department"
                  value={formData.department}
                  onChange={handleChange}
                  className="form-select"
                >
                  <option value="">Select department</option>
                  {DEPARTMENTS.map((dept) => (
                    <option key={dept} value={dept}>
                      {dept}
                    </option>
                  ))}
                </select>
              </div>

              {/* Country */}
              <div className="form-group">
                <label htmlFor="country" className="form-label">
                  Country
                </label>
                <select
                  id="country"
                  name="country"
                  value={formData.country}
                  onChange={handleChange}
                  className="form-select"
                >
                  {COUNTRIES.map((country) => (
                    <option key={country} value={country}>
                      {country}
                    </option>
                  ))}
                </select>
              </div>

              {/* Employment Type */}
              <div className="form-group">
                <label htmlFor="employment_type" className="form-label">
                  Employment Type
                </label>
                <select
                  id="employment_type"
                  name="employment_type"
                  value={formData.employment_type}
                  onChange={handleChange}
                  className="form-select"
                >
                  {EMPLOYMENT_TYPES.map((type) => (
                    <option key={type} value={type}>
                      {type.replace('_', ' ')}
                    </option>
                  ))}
                </select>
              </div>

              {/* Hire Date */}
              <div className="form-group">
                <label htmlFor="hire_date" className="form-label">
                  Hire Date
                </label>
                <input
                  id="hire_date"
                  type="date"
                  name="hire_date"
                  value={formData.hire_date}
                  onChange={handleChange}
                  className="form-input"
                />
              </div>

              {/* Salary */}
              <div className="form-group">
                <label htmlFor="salary" className="form-label">
                  Annual Salary *
                </label>
                <input
                  id="salary"
                  type="number"
                  name="salary"
                  value={formData.salary}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="0.00"
                  step="0.01"
                  min="0"
                  required
                />
              </div>

              {/* Currency */}
              <div className="form-group">
                <label htmlFor="currency" className="form-label">
                  Currency
                </label>
                <select
                  id="currency"
                  name="currency"
                  value={formData.currency}
                  onChange={handleChange}
                  className="form-select"
                >
                  <option value="USD">USD</option>
                  <option value="EUR">EUR</option>
                  <option value="GBP">GBP</option>
                  <option value="INR">INR</option>
                  <option value="AUD">AUD</option>
                  <option value="CAD">CAD</option>
                  <option value="JPY">JPY</option>
                  <option value="SEK">SEK</option>
                </select>
              </div>
            </div>

            {/* Submit */}
            <div style={{ display: 'flex', gap: '12px', marginTop: '32px', paddingTop: '24px', borderTop: '1px solid #e2e8f0' }}>
              <button
                type="submit"
                disabled={isPending}
                className="btn btn-primary"
                style={{ flex: 1 }}
              >
                {isPending ? 'Creating...' : 'Create Employee'}
              </button>
              <Link
                to="/"
                className="btn btn-secondary"
                style={{ flex: 1, justifyContent: 'center' }}
              >
                Cancel
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
