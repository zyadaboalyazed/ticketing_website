import api from './api';
import { Ticket } from '../types';

export const ticketService = {
  async getTickets(params?: { status?: string; priority?: string }) {
    const response = await api.get('/tickets/', { params });
    return response.data;
  },

  async getTicket(id: number): Promise<Ticket> {
    const response = await api.get(`/tickets/${id}`);
    return response.data;
  },

  async createTicket(ticketData: {
    title: string;
    description?: string;
    priority?: string;
    contract_id?: number;
  }) {
    const response = await api.post('/tickets/', ticketData);
    return response.data;
  },

  async updateTicket(id: number, ticketData: any) {
    const response = await api.put(`/tickets/${id}`, ticketData);
    return response.data;
  },

  async deleteTicket(id: number) {
    await api.delete(`/tickets/${id}`);
  },

  async getComments(ticketId: number) {
    const response = await api.get(`/tickets/${ticketId}/comments`);
    return response.data;
  },

  async addComment(ticketId: number, content: string, isInternal: boolean = false) {
    const response = await api.post(`/tickets/${ticketId}/comments`, {
      content,
      is_internal: isInternal ? 1 : 0,
    });
    return response.data;
  },
};
