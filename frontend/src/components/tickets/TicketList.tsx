import React, { useEffect, useState } from 'react';
import { ticketService } from '../../services/ticket.service';
import { Ticket, TicketStatus } from '../../types/ticket';
import { useAuth } from '../../contexts/AuthContext';
import { UserRole } from '../../types/auth';
import { Link } from 'react-router-dom';
import './Tickets.css';

const TicketList: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [statusFilter, setStatusFilter] = useState<TicketStatus | ''>('');
  const { user } = useAuth();

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      setLoading(true);
      const data = await ticketService.getTickets();
      setTickets(data);
    } catch (err: any) {
      setError('Failed to load tickets');
    } finally {
      setLoading(false);
    }
  };

  const filteredTickets = statusFilter
    ? tickets.filter((t) => t.status === statusFilter)
    : tickets;

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'red';
      case 'high': return 'orange';
      case 'medium': return 'yellow';
      case 'low': return 'green';
      default: return 'gray';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return '#3498db';
      case 'in_progress': return '#f39c12';
      case 'resolved': return '#2ecc71';
      case 'closed': return '#95a5a6';
      case 'on_hold': return '#e74c3c';
      default: return 'gray';
    }
  };

  if (loading) return <div className="loading">Loading tickets...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="tickets-container">
      <div className="tickets-header">
        <h1>Tickets</h1>
        {user?.role === UserRole.CLIENT && (
          <Link to="/tickets/new" className="btn-primary">Create Ticket</Link>
        )}
      </div>

      <div className="filters">
        <label>
          Filter by Status:
          <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value as any)}>
            <option value="">All</option>
            <option value={TicketStatus.OPEN}>Open</option>
            <option value={TicketStatus.IN_PROGRESS}>In Progress</option>
            <option value={TicketStatus.RESOLVED}>Resolved</option>
            <option value={TicketStatus.CLOSED}>Closed</option>
            <option value={TicketStatus.ON_HOLD}>On Hold</option>
          </select>
        </label>
      </div>

      <div className="tickets-list">
        {filteredTickets.length === 0 ? (
          <p>No tickets found</p>
        ) : (
          <table className="tickets-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Status</th>
                <th>Priority</th>
                <th>Price</th>
                <th>Created</th>
                <th>SLA</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredTickets.map((ticket) => (
                <tr key={ticket.id}>
                  <td>#{ticket.id}</td>
                  <td>{ticket.title}</td>
                  <td>
                    <span
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(ticket.status) }}
                    >
                      {ticket.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td>
                    <span
                      className="priority-badge"
                      style={{ backgroundColor: getPriorityColor(ticket.priority) }}
                    >
                      {ticket.priority}
                    </span>
                  </td>
                  <td>${ticket.final_price.toFixed(2)}</td>
                  <td>{new Date(ticket.created_at).toLocaleDateString()}</td>
                  <td>
                    {ticket.sla_breached ? (
                      <span className="sla-badge sla-breached">Breached</span>
                    ) : (
                      <span className="sla-badge sla-ok">OK</span>
                    )}
                  </td>
                  <td>
                    <Link to={`/tickets/${ticket.id}`} className="btn-link">View</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default TicketList;
