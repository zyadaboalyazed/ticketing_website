import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ticketService } from '../../services/ticket.service';
import { authService } from '../../services/auth.service';
import { Ticket, TicketStatus, TicketPriority } from '../../types/ticket';
import { User, UserRole } from '../../types/auth';
import { useAuth } from '../../contexts/AuthContext';
import './Tickets.css';

const TicketDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [ticket, setTicket] = useState<Ticket | null>(null);
  const [agents, setAgents] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: TicketPriority.MEDIUM,
    status: TicketStatus.OPEN,
    assigned_agent_id: 0,
  });

  useEffect(() => {
    if (id) {
      loadTicket(parseInt(id));
      if (user?.role === UserRole.ADMIN || user?.role === UserRole.AGENT) {
        loadAgents();
      }
    }
  }, [id]);

  const loadTicket = async (ticketId: number) => {
    try {
      setLoading(true);
      const data = await ticketService.getTicket(ticketId);
      setTicket(data);
      setFormData({
        title: data.title,
        description: data.description,
        priority: data.priority,
        status: data.status,
        assigned_agent_id: data.assigned_agent_id || 0,
      });
    } catch (err: any) {
      setError('Failed to load ticket');
    } finally {
      setLoading(false);
    }
  };

  const loadAgents = async () => {
    try {
      const users = await authService.getUsers();
      setAgents(users.filter((u) => u.role === UserRole.AGENT));
    } catch (err) {
      console.error('Failed to load agents');
    }
  };

  const handleUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!ticket) return;

    try {
      const updateData: any = {};
      if (formData.title !== ticket.title) updateData.title = formData.title;
      if (formData.description !== ticket.description) updateData.description = formData.description;
      if (formData.priority !== ticket.priority) updateData.priority = formData.priority;
      if (formData.status !== ticket.status) updateData.status = formData.status;
      if (formData.assigned_agent_id !== ticket.assigned_agent_id) {
        updateData.assigned_agent_id = formData.assigned_agent_id || null;
      }

      const updated = await ticketService.updateTicket(ticket.id, updateData);
      setTicket(updated);
      setEditing(false);
    } catch (err: any) {
      setError('Failed to update ticket');
    }
  };

  const handleDelete = async () => {
    if (!ticket || !window.confirm('Are you sure you want to delete this ticket?')) return;

    try {
      await ticketService.deleteTicket(ticket.id);
      navigate('/tickets');
    } catch (err: any) {
      setError('Failed to delete ticket');
    }
  };

  if (loading) return <div className="loading">Loading ticket...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!ticket) return <div>Ticket not found</div>;

  const canEdit = user?.role === UserRole.ADMIN || 
                  user?.role === UserRole.AGENT || 
                  (user?.role === UserRole.CLIENT && ticket.client_id === user.id);

  return (
    <div className="ticket-detail">
      <div className="ticket-header">
        <h1>Ticket #{ticket.id}</h1>
        <div className="ticket-actions">
          {canEdit && !editing && (
            <button onClick={() => setEditing(true)} className="btn-secondary">Edit</button>
          )}
          {user?.role === UserRole.ADMIN && (
            <button onClick={handleDelete} className="btn-danger">Delete</button>
          )}
          <button onClick={() => navigate('/tickets')} className="btn-secondary">Back</button>
        </div>
      </div>

      {editing ? (
        <form onSubmit={handleUpdate} className="ticket-form">
          <div className="form-group">
            <label>Title</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows={5}
              required
            />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value as TicketPriority })}
              >
                <option value={TicketPriority.LOW}>Low</option>
                <option value={TicketPriority.MEDIUM}>Medium</option>
                <option value={TicketPriority.HIGH}>High</option>
                <option value={TicketPriority.CRITICAL}>Critical</option>
              </select>
            </div>
            {(user?.role === UserRole.ADMIN || user?.role === UserRole.AGENT) && (
              <>
                <div className="form-group">
                  <label>Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value as TicketStatus })}
                  >
                    <option value={TicketStatus.OPEN}>Open</option>
                    <option value={TicketStatus.IN_PROGRESS}>In Progress</option>
                    <option value={TicketStatus.RESOLVED}>Resolved</option>
                    <option value={TicketStatus.CLOSED}>Closed</option>
                    <option value={TicketStatus.ON_HOLD}>On Hold</option>
                  </select>
                </div>
                <div className="form-group">
                  <label>Assigned Agent</label>
                  <select
                    value={formData.assigned_agent_id}
                    onChange={(e) => setFormData({ ...formData, assigned_agent_id: parseInt(e.target.value) })}
                  >
                    <option value={0}>Unassigned</option>
                    {agents.map((agent) => (
                      <option key={agent.id} value={agent.id}>
                        {agent.full_name || agent.username}
                      </option>
                    ))}
                  </select>
                </div>
              </>
            )}
          </div>
          <div className="form-actions">
            <button type="submit" className="btn-primary">Save Changes</button>
            <button type="button" onClick={() => setEditing(false)} className="btn-secondary">
              Cancel
            </button>
          </div>
        </form>
      ) : (
        <div className="ticket-info">
          <div className="info-grid">
            <div className="info-item">
              <label>Title:</label>
              <span>{ticket.title}</span>
            </div>
            <div className="info-item">
              <label>Status:</label>
              <span className="badge">{ticket.status.replace('_', ' ')}</span>
            </div>
            <div className="info-item">
              <label>Priority:</label>
              <span className="badge">{ticket.priority}</span>
            </div>
            <div className="info-item">
              <label>Price:</label>
              <span>${ticket.final_price.toFixed(2)}</span>
            </div>
            <div className="info-item">
              <label>SLA Status:</label>
              <span className={ticket.sla_breached ? 'badge-danger' : 'badge-success'}>
                {ticket.sla_breached ? 'Breached' : 'OK'}
              </span>
            </div>
            <div className="info-item">
              <label>Created:</label>
              <span>{new Date(ticket.created_at).toLocaleString()}</span>
            </div>
            {ticket.due_date && (
              <div className="info-item">
                <label>Due Date:</label>
                <span>{new Date(ticket.due_date).toLocaleString()}</span>
              </div>
            )}
            {ticket.resolved_at && (
              <div className="info-item">
                <label>Resolved:</label>
                <span>{new Date(ticket.resolved_at).toLocaleString()}</span>
              </div>
            )}
          </div>
          <div className="info-item full-width">
            <label>Description:</label>
            <p className="description">{ticket.description}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default TicketDetail;
