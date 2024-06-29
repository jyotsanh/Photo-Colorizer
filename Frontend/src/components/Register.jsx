// src/components/Register.js
import React, { useState } from 'react';
import { registerUser } from '../services/api';
import "./register/register.css";

import Cookies from 'js-cookie';

function Register() {

    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [errors, setErrors] = useState({});
    const validateEmail = (email) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    };

    const validatePassword = (password) => {
        const passwordRegex = /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;
        return passwordRegex.test(password);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSuccessMessage("")
        setErrors({});
        console.log(email, username, first_name, last_name, password, password2);
        const formData = {
            "email":email,
            "username":username,
            "first_name":first_name,
            "last_name":last_name,
            "password":password,
            "password2":password2
        }
        try{
            const response = await registerUser(formData);
            if (response.status == 'success'){
                console.log("completed")
                setSuccessMessage("SIGNED UP SUCCESSFULLY");
            }
            
            console.log("response:")
            const {msg} = response.data //->registration succesfull
            const {token} = response.data 

            if (token) {
                const { access, refresh } = token; //-> token fetched
                console.log(access);

                // Store the tokens in cookies
                Cookies.set('accessToken', access);
                Cookies.set('refreshToken', refresh);
            } else {
                console.log("Tokens are not coming");
            }
            
        } catch(error){
            const {data } = error.response
            const error_msg = data.errors
            console.log('Sign-up email error:', error_msg.email);
            console.log('Sign-up username error:', error_msg.username);
            console.log('Sign-up pswd error:', error_msg.non_field_errors);
            setErrors({ email: error_msg.email, username: error_msg.username, password: error_msg.non_field_errors });
        }
        
    }
    return (
        <div>
        <form onSubmit={handleSubmit}>
            <input 
            type="email" 
            name="email" 
            placeholder="Email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            />
            {errors.email && <p className="error-text">{errors.email}</p>}


            <input 
            type="text" 
            name="username" 
            placeholder="Username" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
            />
            {errors.username && <p className="error-text">{errors.username}</p>}


            <input 
            type="text" 
            name="first_name" 
            placeholder="First Name" 
            value={first_name} 
            onChange={(e) => setFirstName(e.target.value)} 
            required 
            />
            <input 
            type="text" 
            name="last_name" 
            placeholder="Last Name" 
            value={last_name} 
            onChange={(e) => setLastName(e.target.value)} 
            required 
            />

            <input type="password" name="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <input 
            type="password" 
            name="password2" 
            placeholder="Confirm Password" 
            value={password2} 
            onChange={(e) => setPassword2(e.target.value)} 
            required 
            />
            {errors.password && <p className="error-text">{errors.password}</p>}
            {successMessage && <p className="success-text">{successMessage}</p>}

            <button type="submit" onClick={handleSubmit}>Register</button>
            <a className="link-text" href='/login'>Already have an account? Log in</a>
        </form>
        </div>
    );
};

export default Register;
