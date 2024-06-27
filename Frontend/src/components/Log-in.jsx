// src/components/Login.js
import React, { useState } from 'react';
import { loginUser } from '../services/api';
import Register from './Register.jsx';

const Login = ({ onLogin }) => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });


    return (
        <form onSubmit={handleSubmit}>
            <input type="email" name="email" placeholder="Email" onChange={handleChange} />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} />
            <button type="submit">Login</button>
            <button onClick={Register}>Register</button>
        </form>
    );
};

export default Login;
