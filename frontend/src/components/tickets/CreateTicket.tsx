import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ticketService } from '../../services/ticket.service';
import { contractService } from '../../services/contract.service';
import { TicketPriority } from '../../types/ticket';
import { Contract } from '../../types/contract';
import './Tickets.css';

const CreateTicket: React.FC = () => {
  const navigate = useNavigate();
  const [contracts, setContracts] = useState<Contract[]>([]);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: TicketPriority.MEDIUM,
    contract_id: 0,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadContracts();
  }, []);

  const loadContracts = async () => {
    try {
      const data = await contractService.getContracts();
      setContracts(data.filter((c) => c.is_active));
    } catch (err) {
      console.error('Failed to load contracts');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const ticketData = {
        title: formData.title,
        description: formData.description,
        priority: formData.priority,
        contract_id: formData.contract_id || undefined,
      };
      const created = await ticketService.createTicket(ticketData);
      navigate(`/tickets/${created.id}`);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create ticket');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="create-ticket">
      <h1>Create New Ticket</h1>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="ticket-form">
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="description">Description *</label>
          <textarea
            id="description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={6}
            required
          />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="priority">Priority</label>
            <select
              id="priority"
              value={formData.priority}
              onChange={(e) => setFormData({ ...formData, priority: e.target.value as TicketPriority })}
            >
              <option value={TicketPriority.LOW}>Low</option>
              <option value={TicketPriority.MEDIUM}>Medium</option>
              <option value={TicketPriority.HIGH}>High</option>
              <option value={TicketPriority.CRITICAL}>Critical</option>
            </select>
          </div>
          {contracts.length > 0 && (
            <div className="form-group">
              <label htmlFor="contract">Contract (Optional)</label>
              <select
                id="contract"
                value={formData.contract_id}
                onChange={(e) => setFormData({ ...formData, contract_id: parseInt(e.target.value) })}
              >
                <option value={0}>No Contract</option>
                {contracts.map((contract) => (
                  <option key={contract.id} value={contract.id}>
                    {contract.name}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
        <div className="form-actions">
          <button type="submit" disabled={loading} className="btn-primary">
            {loading ? 'Creating...' : 'Create Ticket'}
          </button>
          <button type="button" onClick={() => navigate('/tickets')} className="btn-secondary">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateTicket;
