import { useInsights } from '../api/hooks';
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { TrendingUp, Users, DollarSign } from 'lucide-react';

const COLORS = ['#2563eb', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#06b6d4'];

export default function InsightsDashboardPage() {
  const { data: insights, isLoading, error } = useInsights();

  if (isLoading) return <div className="loading" />;
  if (error || !insights) return <div className="error">Error loading insights</div>;

  const formatCurrency = (value: number | string) => {
    const num = typeof value === 'string' ? parseFloat(value) : value;
    if (isNaN(num)) return '$0';
    return `$${num.toLocaleString('en-US', { maximumFractionDigits: 0 })}`;
  };

  const headlineCards = [
    {
      label: 'Total Headcount',
      value: insights.headline.headcount,
      icon: Users,
      color: '#2563eb',
    },
    {
      label: 'Total Payroll (USD)',
      value: formatCurrency(insights.headline.total_payroll_usd),
      icon: DollarSign,
      color: '#10b981',
    },
    {
      label: 'Avg Salary (USD)',
      value: formatCurrency(insights.headline.avg_salary_usd),
      icon: TrendingUp,
      color: '#f59e0b',
    },
    {
      label: 'Median Salary (USD)',
      value: formatCurrency(insights.headline.median_salary_usd),
      icon: DollarSign,
      color: '#8b5cf6',
    },
  ];

  const byCountry = (insights.by_country || []).map((item) => ({
    ...item,
    avg_salary_usd: Math.round(typeof item.avg_salary_usd === 'string' ? parseFloat(item.avg_salary_usd) : item.avg_salary_usd),
  }));

  const byDepartment = (insights.by_department || []).map((item) => ({
    ...item,
    avg_salary_usd: Math.round(typeof item.avg_salary_usd === 'string' ? parseFloat(item.avg_salary_usd) : item.avg_salary_usd),
  }));

  const byTitle = (insights.by_job_title || []).map((item) => ({
    ...item,
    avg_salary_usd: Math.round(typeof item.avg_salary_usd === 'string' ? parseFloat(item.avg_salary_usd) : item.avg_salary_usd),
  }));

  const CustomPieTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length > 0) {
      const data = payload[0].payload;
      const minSalary = formatCurrency(data.min);
      const maxSalary = formatCurrency(data.max);
      const count = payload[0].value;
      return (
        <div style={{
          backgroundColor: '#ffffff',
          border: '1px solid #e2e8f0',
          borderRadius: '8px',
          padding: '12px',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
        }}>
          <p style={{ margin: '0 0 8px 0', fontWeight: '600', color: '#0f172a', fontSize: '14px' }}>
            Salary Range
          </p>
          <p style={{ margin: '0 0 4px 0', color: '#64748b', fontSize: '13px' }}>
            {minSalary} → {maxSalary}
          </p>
          <p style={{ margin: 0, color: '#2563eb', fontWeight: '600', fontSize: '14px' }}>
            {count} employees
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Salary Insights</h1>
        <p className="page-subtitle">Organization-wide compensation analytics</p>
      </div>

      {/* Headline KPI Cards */}
      <div className="kpi-cards-grid">
        {headlineCards.map((card) => {
          const Icon = card.icon;
          return (
            <div key={card.label} className="kpi-card">
              <div style={{ display: 'flex', justifyContent: 'center', marginBottom: '12px' }}>
                <Icon size={28} style={{ color: card.color, opacity: 0.8 }} />
              </div>
              <p className="kpi-card-label">{card.label}</p>
              <p className="kpi-card-value" style={{ color: card.color }}>
                {card.value}
              </p>
            </div>
          );
        })}
      </div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Salary by Country */}
        <div className="chart-container">
          <h3>💼 Salary by Country</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={byCountry} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="country" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                }}
                formatter={(value: any) => formatCurrency(value || 0)}
              />
              <Bar dataKey="avg_salary_usd" fill="#2563eb" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Salary by Department */}
        <div className="chart-container">
          <h3>🏢 Salary by Department</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={byDepartment} margin={{ top: 20, right: 30, left: 0, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis dataKey="department" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                }}
                formatter={(value: any) => formatCurrency(value || 0)}
              />
              <Bar dataKey="avg_salary_usd" fill="#10b981" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Salary by Job Title */}
        <div className="chart-container">
          <h3>👔 Salary by Job Title</h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart
              data={byTitle}
              layout="vertical"
              margin={{ top: 20, right: 30, left: 200, bottom: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis type="number" stroke="#94a3b8" />
              <YAxis dataKey="job_title" type="category" width={190} stroke="#94a3b8" fontSize={12} />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#f8fafc',
                  border: '1px solid #e2e8f0',
                  borderRadius: '8px',
                }}
                formatter={(value: any) => formatCurrency(value || 0)}
              />
              <Bar dataKey="avg_salary_usd" fill="#f59e0b" radius={[0, 8, 8, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Salary Distribution */}
        <div className="chart-container">
          <h3>📊 Salary Distribution</h3>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={insights.distribution || []}
                dataKey="count"
                nameKey="bracket"
                cx="50%"
                cy="50%"
                outerRadius={100}
                label={({ value }: { value: number }) => `${value}`}
              >
                {(insights.distribution || []).map((_: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomPieTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Min/Max Salary Range */}
      <div className="card mb-8">
        <div className="card-header">
          <h2>📈 Salary Range Analysis</h2>
        </div>
        <div className="salary-range-grid">
          <div className="salary-range-box" style={{
            backgroundColor: '#fee2e2',
            borderLeftColor: '#ef4444',
          }}>
            <p className="salary-range-label" style={{ color: '#991b1b' }}>
              Minimum Salary
            </p>
            <p className="salary-range-value" style={{ color: '#991b1b' }}>
              {formatCurrency(insights.headline.min_salary_usd)}
            </p>
          </div>
          <div className="salary-range-box" style={{
            backgroundColor: '#d1fae5',
            borderLeftColor: '#10b981',
          }}>
            <p className="salary-range-label" style={{ color: '#065f46' }}>
              Maximum Salary
            </p>
            <p className="salary-range-value" style={{ color: '#065f46' }}>
              {formatCurrency(insights.headline.max_salary_usd)}
            </p>
          </div>
        </div>
      </div>

      {/* Outliers */}
      <div className="card">
        <div className="card-header">
          <h2>🎯 Salary Outliers</h2>
          <p style={{ margin: 0, fontSize: '13px', color: '#64748b' }}>Employees with salary {'>'} 2 SD from title average</p>
        </div>
        {(insights.outliers || []).length > 0 ? (
          <div className="table-container">
            <table className="table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Job Title</th>
                  <th>Salary (USD)</th>
                  <th>Title Avg (USD)</th>
                  <th>Deviation</th>
                </tr>
              </thead>
              <tbody>
                {(insights.outliers || []).map((outlier) => {
                  const salaryUsd = typeof outlier.salary_usd === 'string' ? parseFloat(outlier.salary_usd) : outlier.salary_usd;
                  const titleAvgUsd = typeof outlier.avg_for_title_usd === 'string' ? parseFloat(outlier.avg_for_title_usd) : outlier.avg_for_title_usd;
                  const deviationFromAvg = typeof outlier.deviation_from_avg === 'string' ? parseFloat(outlier.deviation_from_avg) : outlier.deviation_from_avg;
                  return (
                    <tr key={outlier.id}>
                      <td>
                        <strong>{outlier.name}</strong>
                      </td>
                      <td>{outlier.job_title}</td>
                      <td>{formatCurrency(salaryUsd)}</td>
                      <td>{formatCurrency(titleAvgUsd)}</td>
                      <td>
                        <span
                          className={`badge ${
                            deviationFromAvg > 0
                              ? 'badge-success'
                              : 'badge-danger'
                          }`}
                        >
                          {deviationFromAvg > 0 ? '+' : ''}
                          {deviationFromAvg.toFixed(1)}%
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        ) : (
          <p style={{ color: '#64748b', margin: 0 }}>No outliers detected</p>
        )}
      </div>
    </div>
  );
}
