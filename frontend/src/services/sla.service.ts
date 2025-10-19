import { apiClient } from './api';
import { SLA, SLACreate, SLAUpdate } from '../types/sla';

export const slaService = {
  async getSLAs(): Promise<SLA[]> {
    const response = await apiClient.get<SLA[]>('/slas');
    return response.data;
  },

  async getSLA(id: number): Promise<SLA> {
    const response = await apiClient.get<SLA>(`/slas/${id}`);
    return response.data;
  },

  async createSLA(data: SLACreate): Promise<SLA> {
    const response = await apiClient.post<SLA>('/slas', data);
    return response.data;
  },

  async updateSLA(id: number, data: SLAUpdate): Promise<SLA> {
    const response = await apiClient.put<SLA>(`/slas/${id}`, data);
    return response.data;
  },

  async deleteSLA(id: number): Promise<void> {
    await apiClient.delete(`/slas/${id}`);
  },
};
