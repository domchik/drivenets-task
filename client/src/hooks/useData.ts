import { useState } from 'react';
import { DataItem } from '../types';
import * as dataService from '../services/dataService';

interface UseDataReturn {
  data: DataItem[];
  fetchData: (token: string) => Promise<void>;
  error: string;
  loading: boolean;
}

export const useData = (): UseDataReturn => {
  const [data, setData] = useState<DataItem[]>([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchData = async (token: string): Promise<void> => {
    if (!token) return;

    setLoading(true);
    try {
      const fetchedData = await dataService.fetchProtectedData(token);
      setData(fetchedData);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data. Your session might have expired.');
    } finally {
      setLoading(false);
    }
  };

  return {
    data,
    fetchData,
    error,
    loading
  };
}; 