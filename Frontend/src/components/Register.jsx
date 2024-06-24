// src/components/Register.js
import React, { useState } from 'react';
import { registerUser } from '../services/api';

const Register = () => {
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        password2: '',
    });

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await registerUser(formData);
            console.log('Registration successful', response);
        } catch (error) {
            console.error('Error registering user', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input type="email" name="email" placeholder="Email" onChange={handleChange} />
            <input type="text" name="username" placeholder="Username" onChange={handleChange} />
            <input type="text" name="first_name" placeholder="First Name" onChange={handleChange} />
            <input type="text" name="last_name" placeholder="Last Name" onChange={handleChange} />
            <input type="password" name="password" placeholder="Password" onChange={handleChange} />
            <input type="password" name="password2" placeholder="Confirm Password" onChange={handleChange} />
            <button type="submit">Register</button>
        </form>
    );
};

export default Register;
