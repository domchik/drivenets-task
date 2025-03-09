import React from 'react';
import { useAuth } from '../hooks/useAuth';
import { useData } from '../hooks/useData';
import LoginForm from '../components/LoginForm';
import Dashboard from '../components/Dashboard';

const HomePage: React.FC = () => {
  const { user, login, logout, error: authError, loading: authLoading } = useAuth();
  const { data, fetchData, loading: dataLoading } = useData();

  const handleFetchData = async () => {
    if (user) {
      await fetchData(user.token);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>React Auth Demo for Drivenets</h1>
        
        {!user ? (
          <LoginForm 
            onLogin={login} 
            loading={authLoading} 
            error={authError} 
          />
        ) : (
          <Dashboard 
            user={user} 
            data={data} 
            onFetchData={handleFetchData} 
            onLogout={logout} 
            loading={dataLoading} 
          />
        )}
      </header>
    </div>
  );
};

export default HomePage; 