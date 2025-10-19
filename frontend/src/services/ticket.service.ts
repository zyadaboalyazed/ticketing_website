import { apiClient } from './api';
import { Ticket, TicketCreate, TicketUpdate } from '../types/ticket';

export const ticketService = {
  async getTickets(): Promise<Ticket[]> {
    const response = await apiClient.get<Ticket[]>('/tickets');
    return response.data;
  },

  async getTicket(id: number): Promise<Ticket> {
    const response = await apiClient.get<Ticket>(`/tickets/${id}`);
    return response.data;
  },

  async createTicket(data: TicketCreate): Promise<Ticket> {
    const response = await apiClient.post<Ticket>('/tickets', data);
    return response.data;
  },

  async updateTicket(id: number, data: TicketUpdate): Promise<Ticket> {
    const response = await apiClient.put<Ticket>(`/tickets/${id}`, data);
    return response.data;
  },

  async deleteTicket(id: number): Promise<void> {
    await apiClient.delete(`/tickets/${id}`);
  },

  async downloadTicketsPDF(): Promise<Blob> {
    const response = await apiClient.get('/reports/tickets/pdf', {
      responseType: 'blob',
    });
    return response.data;
  },

  async downloadTicketsCSV(): Promise<Blob> {
    const response = await apiClient.get('/reports/tickets/csv', {
      responseType: 'blob',
    });
    return response.data;
  },
};
