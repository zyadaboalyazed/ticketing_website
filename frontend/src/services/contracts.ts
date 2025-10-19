import api from './api';

export const contractService = {
  async getContracts() {
    const response = await api.get('/contracts/');
    return response.data;
  },

  async getContract(id: number) {
    const response = await api.get(`/contracts/${id}`);
    return response.data;
  },

  async createContract(contractData: any) {
    const response = await api.post('/contracts/', contractData);
    return response.data;
  },

  async updateContract(id: number, contractData: any) {
    const response = await api.put(`/contracts/${id}`, contractData);
    return response.data;
  },

  async deleteContract(id: number) {
    await api.delete(`/contracts/${id}`);
  },
};
