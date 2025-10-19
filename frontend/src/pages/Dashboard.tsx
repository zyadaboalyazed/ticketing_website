import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { ticketService } from '../services/tickets';
import { contractService } from '../services/contracts';
import { Ticket } from '../types';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [contracts, setContracts] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateTicket, setShowCreateTicket] = useState(false);
  const [newTicket, setNewTicket] = useState({
    title: '',
    description: '',
    priority: 'medium',
    contract_id: undefined as number | undefined,
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [ticketsData, contractsData] = await Promise.all([
        ticketService.getTickets(),
        contractService.getContracts(),
      ]);
      setTickets(ticketsData);
      setContracts(contractsData);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await ticketService.createTicket(newTicket);
      setShowCreateTicket(false);
      setNewTicket({ title: '', description: '', priority: 'medium', contract_id: undefined });
      loadData();
    } catch (error: any) {
      alert(error.response?.data?.detail || 'Failed to create ticket');
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return '#dc3545';
      case 'high': return '#fd7e14';
      case 'medium': return '#ffc107';
      case 'low': return '#28a745';
      default: return '#6c757d';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'open': return '#007bff';
      case 'in_progress': return '#17a2b8';
      case 'pending': return '#ffc107';
      case 'resolved': return '#28a745';
      case 'closed': return '#6c757d';
      default: return '#6c757d';
    }
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Ticketing System Dashboard</h1>
        <div className="user-info">
          <span>Welcome, {user?.full_name || user?.username}</span>
          <span className="role-badge">{user?.role}</span>
          <button onClick={logout} className="btn-logout">Logout</button>
        </div>
      </header>

      <div className="dashboard-content">
        <div className="stats">
          <div className="stat-card">
            <h3>Total Tickets</h3>
            <p className="stat-number">{tickets.length}</p>
          </div>
          <div className="stat-card">
            <h3>Open Tickets</h3>
            <p className="stat-number">
              {tickets.filter(t => t.status === 'open').length}
            </p>
          </div>
          <div className="stat-card">
            <h3>In Progress</h3>
            <p className="stat-number">
              {tickets.filter(t => t.status === 'in_progress').length}
            </p>
          </div>
          <div className="stat-card">
            <h3>Resolved</h3>
            <p className="stat-number">
              {tickets.filter(t => t.status === 'resolved').length}
            </p>
          </div>
        </div>

        <div className="tickets-section">
          <div className="section-header">
            <h2>Tickets</h2>
            <button
              onClick={() => setShowCreateTicket(true)}
              className="btn-create"
            >
              Create Ticket
            </button>
          </div>

          {showCreateTicket && (
            <div className="modal">
              <div className="modal-content">
                <h3>Create New Ticket</h3>
                <form onSubmit={handleCreateTicket}>
                  <div className="form-group">
                    <label>Title</label>
                    <input
                      type="text"
                      value={newTicket.title}
                      onChange={(e) => setNewTicket({ ...newTicket, title: e.target.value })}
                      required
                    />
                  </div>
                  <div className="form-group">
                    <label>Description</label>
                    <textarea
                      value={newTicket.description}
                      onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
                      rows={4}
                    />
                  </div>
                  <div className="form-group">
                    <label>Priority</label>
                    <select
                      value={newTicket.priority}
                      onChange={(e) => setNewTicket({ ...newTicket, priority: e.target.value })}
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="critical">Critical</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Contract</label>
                    <select
                      value={newTicket.contract_id || ''}
                      onChange={(e) => setNewTicket({ 
                        ...newTicket, 
                        contract_id: e.target.value ? parseInt(e.target.value) : undefined 
                      })}
                    >
                      <option value="">No Contract</option>
                      {contracts.map(contract => (
                        <option key={contract.id} value={contract.id}>
                          {contract.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="modal-actions">
                    <button type="submit" className="btn-primary">Create</button>
                    <button
                      type="button"
                      onClick={() => setShowCreateTicket(false)}
                      className="btn-secondary"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          )}

          <div className="tickets-list">
            {tickets.length === 0 ? (
              <p className="no-tickets">No tickets found</p>
            ) : (
              tickets.map(ticket => (
                <div key={ticket.id} className="ticket-card">
                  <div className="ticket-header">
                    <h3>#{ticket.id} - {ticket.title}</h3>
                    <div className="ticket-badges">
                      <span
                        className="badge"
                        style={{ backgroundColor: getPriorityColor(ticket.priority) }}
                      >
                        {ticket.priority}
                      </span>
                      <span
                        className="badge"
                        style={{ backgroundColor: getStatusColor(ticket.status) }}
                      >
                        {ticket.status}
                      </span>
                    </div>
                  </div>
                  <p className="ticket-description">{ticket.description}</p>
                  <div className="ticket-meta">
                    <span>Created: {new Date(ticket.created_at).toLocaleDateString()}</span>
                    {ticket.sla_breached === 1 && (
                      <span className="sla-breach">SLA BREACHED</span>
                    )}
                    {ticket.total_cost > 0 && (
                      <span>Cost: ${ticket.total_cost.toFixed(2)}</span>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {(user?.role === 'admin' || user?.role === 'agent') && (
          <div className="contracts-section">
            <h2>Contracts</h2>
            <div className="contracts-list">
              {contracts.map(contract => (
                <div key={contract.id} className="contract-card">
                  <h3>{contract.name}</h3>
                  <p>{contract.description}</p>
                  <div className="contract-details">
                    <span>Rate: ${contract.hourly_rate}/hr</span>
                    <span>Included Hours: {contract.included_hours}</span>
                    <span>SLA: {contract.resolution_time_hours}hrs</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
