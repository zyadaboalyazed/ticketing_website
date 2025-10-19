import React, { useEffect, useState } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { ticketService } from '../../services/ticket.service';
import { Ticket } from '../../types/ticket';
import { UserRole } from '../../types/auth';
import { Link } from 'react-router-dom';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      const data = await ticketService.getTickets();
      setTickets(data);
    } catch (err) {
      console.error('Failed to load tickets');
    } finally {
      setLoading(false);
    }
  };

  const stats = {
    total: tickets.length,
    open: tickets.filter((t) => t.status === 'open').length,
    inProgress: tickets.filter((t) => t.status === 'in_progress').length,
    resolved: tickets.filter((t) => t.status === 'resolved').length,
    breached: tickets.filter((t) => t.sla_breached).length,
    totalValue: tickets.reduce((sum, t) => sum + t.final_price, 0),
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <h1>Welcome, {user?.full_name || user?.username}!</h1>
      <p className="role-badge">Role: {user?.role}</p>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Tickets</h3>
          <p className="stat-value">{stats.total}</p>
        </div>
        <div className="stat-card">
          <h3>Open</h3>
          <p className="stat-value">{stats.open}</p>
        </div>
        <div className="stat-card">
          <h3>In Progress</h3>
          <p className="stat-value">{stats.inProgress}</p>
        </div>
        <div className="stat-card">
          <h3>Resolved</h3>
          <p className="stat-value">{stats.resolved}</p>
        </div>
        <div className="stat-card alert">
          <h3>SLA Breached</h3>
          <p className="stat-value">{stats.breached}</p>
        </div>
        <div className="stat-card">
          <h3>Total Value</h3>
          <p className="stat-value">${stats.totalValue.toFixed(2)}</p>
        </div>
      </div>

      <div className="quick-actions">
        <h2>Quick Actions</h2>
        <div className="action-buttons">
          <Link to="/tickets" className="action-btn">View All Tickets</Link>
          {user?.role === UserRole.CLIENT && (
            <Link to="/tickets/new" className="action-btn">Create Ticket</Link>
          )}
          {user?.role === UserRole.ADMIN && (
            <>
              <Link to="/contracts" className="action-btn">Manage Contracts</Link>
              <Link to="/slas" className="action-btn">Manage SLAs</Link>
              <Link to="/reports" className="action-btn">View Reports</Link>
            </>
          )}
          {user?.role === UserRole.AGENT && (
            <Link to="/reports" className="action-btn">View Reports</Link>
          )}
        </div>
      </div>

      <div className="recent-tickets">
        <h2>Recent Tickets</h2>
        {tickets.slice(0, 5).map((ticket) => (
          <div key={ticket.id} className="ticket-card">
            <div className="ticket-card-header">
              <h3>
                <Link to={`/tickets/${ticket.id}`}>#{ticket.id} - {ticket.title}</Link>
              </h3>
              <span className={`status-badge ${ticket.status}`}>{ticket.status}</span>
            </div>
            <p>{ticket.description.substring(0, 100)}...</p>
            <div className="ticket-card-footer">
              <span>Priority: {ticket.priority}</span>
              <span>Price: ${ticket.final_price.toFixed(2)}</span>
              {ticket.sla_breached && <span className="sla-alert">SLA Breached</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
