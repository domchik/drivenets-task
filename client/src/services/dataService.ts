import axios from 'axios';
import { ApiResponse, DataItem } from '../types';

export const fetchProtectedData = async (token: string): Promise<DataItem[]> => {
  const response = await axios.get<ApiResponse<DataItem[]>>('/api/data', {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  
  return response.data.data;
}; 