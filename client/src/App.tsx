import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import './App.css';

interface User {
  username: string;
  token: string;
}

// Cookie options
const COOKIE_OPTIONS = {
  expires: 1, // 1 day
  path: '/',
  sameSite: 'strict' as const
};

// Cookie name
const TOKEN_COOKIE = 'auth_token';
const USERNAME_COOKIE = 'auth_username';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any[]>([]);

  // Check if user is already logged in
  useEffect(() => {
    const storedToken = Cookies.get(TOKEN_COOKIE);
    const storedUsername = Cookies.get(USERNAME_COOKIE);
    
    if (storedToken && storedUsername) {
      setUser({
        username: storedUsername,
        token: storedToken
      });
    }
  }, []);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await axios.post('/auth/login', {
        username,
        password
      });

      const token = response.data.token;
      
      // Save user data in cookies
      Cookies.set(TOKEN_COOKIE, token, COOKIE_OPTIONS);
      Cookies.set(USERNAME_COOKIE, username, COOKIE_OPTIONS);
      
      setUser({
        username,
        token
      });
      
      setUsername('');
      setPassword('');
    } catch (err) {
      setError('Invalid credentials. Please try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    // Remove cookies
    Cookies.remove(TOKEN_COOKIE);
    Cookies.remove(USERNAME_COOKIE);
    
    setUser(null);
    setData([]);
  };

  const fetchData = async () => {
    if (!user) return;

    setLoading(true);
    try {
      const response = await axios.get('/api/data', {
        headers: {
          Authorization: `Bearer ${user.token}`
        }
      });
      setData(response.data.data);
    } catch (err) {
      console.error('Error fetching data:', err);
      setError('Failed to fetch data. Your session might have expired.');
      // If token is invalid, log the user out
      if (axios.isAxiosError(err) && err.response?.status === 401) {
        handleLogout();
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Auth Demo for Drivenets</h1>
        
        {error && <div className="error-message">{error}</div>}
        
        {!user ? (
          <div className="login-container">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label htmlFor="username">Username:</label>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">Password:</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </div>
              <button type="submit" disabled={loading}>
                {loading ? 'Logging in...' : 'Login'}
              </button>
            </form>
            <p className="hint">Try user1/password1 or user2/password2</p>
          </div>
        ) : (
          <div className="dashboard">
            <h2>Welcome, {user.username}!</h2>
            <div className="actions">
              <button onClick={fetchData} disabled={loading}>
                {loading ? 'Loading...' : 'Fetch Protected Data'}
              </button>
              <button onClick={handleLogout}>Logout</button>
            </div>
            
            {data.length > 0 && (
              <div className="data-container">
                <h3>Protected Data:</h3>
                <ul>
                  {data.map((item) => (
                    <li key={item.id}>{item.name}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
