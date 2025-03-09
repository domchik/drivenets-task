import axios from 'axios';
import Cookies from 'js-cookie';
import { LoginCredentials, User } from '../types';

// Cookie options
const COOKIE_OPTIONS = {
  expires: 1, // 1 day
  path: '/',
  sameSite: 'strict' as const
};

// Cookie names
export const TOKEN_COOKIE = 'auth_token';
export const USERNAME_COOKIE = 'auth_username';

export const login = async (credentials: LoginCredentials): Promise<User> => {
  const response = await axios.post('/auth/login', credentials);
  const token = response.data.token;
  
  // Save user data in cookies
  Cookies.set(TOKEN_COOKIE, token, COOKIE_OPTIONS);
  Cookies.set(USERNAME_COOKIE, credentials.username, COOKIE_OPTIONS);
  
  return {
    username: credentials.username,
    token
  };
};

export const logout = (): void => {
  // Remove cookies
  Cookies.remove(TOKEN_COOKIE);
  Cookies.remove(USERNAME_COOKIE);
};

export const getCurrentUser = (): User | null => {
  const token = Cookies.get(TOKEN_COOKIE);
  const username = Cookies.get(USERNAME_COOKIE);
  
  if (token && username) {
    return {
      username,
      token
    };
  }
  
  return null;
}; 