import { useParams, Link } from 'react-router-dom';
import { useGetEmployee, useSalaryHistory } from '../api/hooks';
import { ArrowLeft, DollarSign } from 'lucide-react';

export default function EmployeeDetailPage() {
  const { id } = useParams<{ id: string }>();
  const empId = parseInt(id || '0');

  const { data: employee, isLoading: empLoading, error: empError } = useGetEmployee(empId);
  const { data: history, isLoading: histLoading, error: histError } = useSalaryHistory(empId);

  if (empLoading || histLoading) return <div className="loading" />;
  if (empError || histError || !employee) return <div className="error">Error loading employee</div>;

  const formatSalary = (salary: number, currency: string) => {
    return salary.toLocaleString('en-US', {
      style: 'currency',
      currency,
      maximumFractionDigits: 2,
    });
  };

  return (
    <div>
      <Link to="/" className="back-link">
        <ArrowLeft size={18} />
        Back to Employees
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2">
          {/* Employee Info Card */}
          <div className="card card-header">
            <div>
              <h1 className="page-title" style={{ marginBottom: '8px' }}>
                {employee.name}
              </h1>
              <p style={{ color: '#64748b', margin: 0 }}>{employee.email}</p>
            </div>
          </div>

          {/* Details Grid */}
          <div className="card" style={{ marginTop: '24px' }}>
            <div className="card-header">
              <h2>Employee Information</h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <p className="form-label" style={{ marginBottom: '4px' }}>Job Title</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>{employee.job_title}</p>
              </div>
              <div>
                <p className="form-label" style={{ marginBottom: '4px' }}>Department</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>{employee.department}</p>
              </div>
              <div>
                <p className="form-label" style={{ marginBottom: '4px' }}>Country</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>{employee.country}</p>
              </div>
              <div>
                <p className="form-label" style={{ marginBottom: '4px' }}>Employment Type</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>
                  <span className="badge badge-primary">
                    {employee.employment_type.toUpperCase()}
                  </span>
                </p>
              </div>
              <div>
                <p className="form-label" style={{ marginBottom: '4px' }}>Hire Date</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>
                  {new Date(employee.hire_date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
              <div>
                <p className="form-label" style={{ marginBottom: '4px' }}>Status</p>
                <p style={{ margin: 0, fontSize: '16px', fontWeight: '500' }}>
                  <span className={`badge ${
                    employee.status === 'ACTIVE' ? 'badge-success' : 'badge-warning'
                  }`}>
                    {employee.status}
                  </span>
                </p>
              </div>
            </div>
          </div>

          {/* Salary History */}
          <div className="card" style={{ marginTop: '24px' }}>
            <div className="card-header">
              <h2>Salary History</h2>
            </div>

            {history && history.length > 0 ? (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {history.map((record) => (
                  <div
                    key={record.id}
                    style={{
                      borderLeft: '4px solid #2563eb',
                      paddingLeft: '16px',
                      paddingTop: '12px',
                      paddingBottom: '12px',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                      <div>
                        <p style={{ margin: 0, fontSize: '16px', fontWeight: '600', color: '#2563eb' }}>
                          {formatSalary(parseFloat(String(record.new_salary)), record.currency)}
                        </p>
                        <p style={{ margin: '4px 0 0 0', fontSize: '13px', color: '#64748b' }}>
                          {new Date(record.effective_date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                          })}
                        </p>
                        {record.reason && (
                          <p style={{ margin: '8px 0 0 0', fontSize: '14px', color: '#334155' }}>
                            {record.reason}
                          </p>
                        )}
                      </div>
                      {record.old_salary && (
                        <div style={{ textAlign: 'right' }}>
                          <p style={{ margin: 0, fontSize: '12px', color: '#64748b', fontWeight: '500' }}>
                            Previous
                          </p>
                          <p style={{ margin: '4px 0 0 0', fontSize: '14px', fontWeight: '600', color: '#64748b' }}>
                            {formatSalary(parseFloat(String(record.old_salary)), record.currency)}
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p style={{ color: '#64748b', margin: 0 }}>No salary history records yet</p>
            )}
          </div>
        </div>

        {/* Sidebar - Salary Card */}
        <div className="lg:col-span-1">
          <div className="card" style={{
            background: 'linear-gradient(135deg, #2563eb 0%, #1e40af 100%)',
            color: 'white',
            textAlign: 'center',
            borderColor: 'transparent',
          }}>
            <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '12px' }}>
              <DollarSign size={32} style={{ opacity: 0.8 }} />
            </div>
            <p style={{ margin: '0 0 12px 0', opacity: 0.9, fontSize: '14px', fontWeight: '600' }}>
              Current Salary
            </p>
            <p style={{ margin: 0, fontSize: '28px', fontWeight: '700' }}>
              {employee.salary.toLocaleString('en-US', {
                style: 'currency',
                currency: employee.currency,
                maximumFractionDigits: 0,
              })}
            </p>
            <p style={{ margin: '12px 0 0 0', opacity: 0.8, fontSize: '13px' }}>
              {employee.currency}
            </p>

            <div style={{ marginTop: '24px', paddingTop: '24px', borderTop: '1px solid rgba(255,255,255,0.2)' }}>
              <Link
                to={`/employees/${employee.id}/edit`}
                className="btn"
                style={{
                  width: '100%',
                  justifyContent: 'center',
                  backgroundColor: 'white',
                  color: '#2563eb',
                  fontWeight: '600',
                }}
              >
                Edit Salary
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
