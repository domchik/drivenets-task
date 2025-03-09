import { useState, useEffect } from 'react';
import { User, LoginCredentials } from '../types';
import * as authService from '../services/authService';

interface UseAuthReturn {
  user: User | null;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
  error: string;
  loading: boolean;
}

export const useAuth = (): UseAuthReturn => {
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check if user is already logged in
    const currentUser = authService.getCurrentUser();
    if (currentUser) {
      setUser(currentUser);
    }
  }, []);

  const login = async (credentials: LoginCredentials): Promise<void> => {
    setError('');
    setLoading(true);

    try {
      const user = await authService.login(credentials);
      setUser(user);
    } catch (err) {
      setError('Invalid credentials. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  const logout = (): void => {
    authService.logout();
    setUser(null);
  };

  return {
    user,
    login,
    logout,
    error,
    loading
  };
}; 