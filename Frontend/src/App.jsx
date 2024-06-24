import { useState } from 'react'
import Register from './components/Register';
import Login from './components/Log-in';
import Profile from './components/Profile';
import './App.css'

const App = () => {
  const [accessToken, setAccessToken] = useState('');

  const handleLogin = (response) => {
    setAccessToken(response.access_token);  // Store the access token
  };

  return (
    <div className="App">
      <h1>Register</h1>
      <Register />
      <h1>Login</h1>
      <Login onLogin={handleLogin} />
      {accessToken && (
        <>
          <h1>Profile</h1>
          <Profile accessToken={accessToken} />
        </>
      )}
    </div>
  );
};

export default App
