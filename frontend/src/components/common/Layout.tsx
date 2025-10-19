import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { UserRole } from '../../types/auth';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="navbar-brand">
          <Link to="/">Ticketing System</Link>
        </div>
        {user && (
          <>
            <ul className="navbar-menu">
              <li><Link to="/">Dashboard</Link></li>
              <li><Link to="/tickets">Tickets</Link></li>
              {user.role === UserRole.ADMIN && (
                <>
                  <li><Link to="/contracts">Contracts</Link></li>
                  <li><Link to="/slas">SLAs</Link></li>
                  <li><Link to="/users">Users</Link></li>
                  <li><Link to="/reports">Reports</Link></li>
                </>
              )}
              {user.role === UserRole.AGENT && (
                <li><Link to="/reports">Reports</Link></li>
              )}
            </ul>
            <div className="navbar-user">
              <span className="user-info">
                {user.full_name || user.username} ({user.role})
              </span>
              <button onClick={logout} className="btn-logout">Logout</button>
            </div>
          </>
        )}
      </nav>
      <main className="main-content">{children}</main>
    </div>
  );
};

export default Layout;
