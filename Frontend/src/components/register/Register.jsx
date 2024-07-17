import React, { useState } from 'react';
import { registerUser } from '../../services/api';
import "./register.css";
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
        setSuccessMessage("");
        setErrors({});
        console.log(email, username, first_name, last_name, password, password2);
        const formData = {
            email,
            username,
            first_name,
            last_name,
            password,
            password2
        };
        
        try {
            const response = await registerUser(formData);
            const { msg } = response;
            const { token } = response;
            setSuccessMessage(msg);
            if (token) {
                const { access, refresh } = token;
                console.log(access);

                // Store the tokens in cookies
                Cookies.set('accessToken', access);
                Cookies.set('refreshToken', refresh);
            }
        } catch (error) {
            const { data } = error.response;
            const { email, username, non_field_errors } = data.errors;
            setErrors({ email: email, username: username, password: non_field_errors });
        }
    };

    return (
        <div className="regi-container">
            <form className="regi-form" onSubmit={handleSubmit}>
                <h1>Register Here</h1>
                <div className="regi-input-group">
                    <i className="fas fa-envelope regi-icon"></i>
                    <input 
                        type="email" 
                        name="email" 
                        placeholder="Email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                        className="regi-input"
                    />
                </div>
                {errors.email && <p className="regi-error-text">{errors.email}</p>}

                <div className="regi-input-group">
                    <i className="fas fa-user regi-icon"></i>
                    <input 
                        type="text" 
                        name="username" 
                        placeholder="Username" 
                        value={username} 
                        onChange={(e) => setUsername(e.target.value)} 
                        required 
                        className="regi-input"
                    />
                </div>
                {errors.username && <p className="regi-error-text">{errors.username}</p>}

                <div className="regi-input-group">
                    <i className="fas fa-id-badge regi-icon"></i>
                    <input 
                        type="text" 
                        name="first_name" 
                        placeholder="First Name" 
                        value={first_name} 
                        onChange={(e) => setFirstName(e.target.value)} 
                        required 
                        className="regi-input"
                    />
                </div>
                <div className="regi-input-group">
                    <i className="fas fa-id-badge regi-icon"></i>
                    <input 
                        type="text" 
                        name="last_name" 
                        placeholder="Last Name" 
                        value={last_name} 
                        onChange={(e) => setLastName(e.target.value)} 
                        required 
                        className="regi-input"
                    />
                </div>

                <div className="regi-input-group">
                    <i className="fas fa-lock regi-icon"></i>
                    <input 
                        type="password" 
                        name="password" 
                        placeholder="Password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                        className="regi-input"
                    />
                </div>

                <div className="regi-input-group">
                <i className="fas fa-lock regi-icon"></i>
                    <input 
                    
                        type="password" 
                        name="password2" 
                        placeholder="Confirm Password" 
                        value={password2} 
                        onChange={(e) => setPassword2(e.target.value)} 
                        required 
                        className="regi-input"
                    />
                </div>
                {errors.password && <p className="regi-error-text">{errors.password}</p>}
                {successMessage && <p className="regi-success-text">{successMessage}</p>}

                <button type="submit" className="regi-button">Register</button>
                <a className="regi-link-text" href='/login'>Already have an account? Log in</a>
            </form>
        </div>
    );
};

export default Register;
