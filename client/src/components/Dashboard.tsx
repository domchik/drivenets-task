import React from 'react';
import { User, DataItem } from '../types';

interface DashboardProps {
  user: User;
  data: DataItem[];
  onFetchData: () => void;
  onLogout: () => void;
  loading: boolean;
}

const Dashboard: React.FC<DashboardProps> = ({
  user,
  data,
  onFetchData,
  onLogout,
  loading
}) => {
  return (
    <div className="dashboard">
      <h2>Welcome, {user.username}!</h2>
      <div className="actions">
        <button onClick={onFetchData} disabled={loading}>
          {loading ? 'Loading...' : 'Fetch Protected Data'}
        </button>
        <button onClick={onLogout}>Logout</button>
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
  );
};

export default Dashboard; 