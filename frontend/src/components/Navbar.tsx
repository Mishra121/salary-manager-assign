import { Link, useLocation } from 'react-router-dom';
import { BarChart3, Users, Plus } from 'lucide-react';

export default function Navbar() {
  const location = useLocation();

  const isActive = (path: string) => location.pathname === path;

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">
        <BarChart3 size={28} style={{ color: '#60a5fa' }} />
        <span>Salary Manager</span>
      </Link>

      <div className="navbar-links">
        <Link
          to="/"
          className={`navbar-link ${isActive('/') ? 'active' : ''}`}
        >
          <Users size={18} style={{ display: 'inline-block', marginRight: '6px' }} />
          Employees
        </Link>

        <Link
          to="/insights"
          className={`navbar-link ${isActive('/insights') ? 'active' : ''}`}
        >
          <BarChart3 size={18} style={{ display: 'inline-block', marginRight: '6px' }} />
          Insights
        </Link>

        <Link
          to="/create"
          className="navbar-link"
          style={{
            background: '#2563eb',
            color: 'white',
            marginLeft: 'auto',
          }}
        >
          <Plus size={18} style={{ display: 'inline-block', marginRight: '6px' }} />
          Add Employee
        </Link>
      </div>
    </nav>
  );
}
