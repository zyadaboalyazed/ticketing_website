import { apiClient } from './api';
import { Contract, ContractCreate, ContractUpdate } from '../types/contract';

export const contractService = {
  async getContracts(): Promise<Contract[]> {
    const response = await apiClient.get<Contract[]>('/contracts');
    return response.data;
  },

  async getContract(id: number): Promise<Contract> {
    const response = await apiClient.get<Contract>(`/contracts/${id}`);
    return response.data;
  },

  async createContract(data: ContractCreate): Promise<Contract> {
    const response = await apiClient.post<Contract>('/contracts', data);
    return response.data;
  },

  async updateContract(id: number, data: ContractUpdate): Promise<Contract> {
    const response = await apiClient.put<Contract>(`/contracts/${id}`, data);
    return response.data;
  },

  async deleteContract(id: number): Promise<void> {
    await apiClient.delete(`/contracts/${id}`);
  },

  async downloadContractsPDF(): Promise<Blob> {
    const response = await apiClient.get('/reports/contracts/pdf', {
      responseType: 'blob',
    });
    return response.data;
  },

  async downloadContractsCSV(): Promise<Blob> {
    const response = await apiClient.get('/reports/contracts/csv', {
      responseType: 'blob',
    });
    return response.data;
  },
};
