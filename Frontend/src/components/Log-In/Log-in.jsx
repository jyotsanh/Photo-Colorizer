import React, { useState } from 'react';
import { loginUser } from '../../services/api';
import { useNavigate } from 'react-router-dom';
import Cookies from 'js-cookie';
import './Log.css';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errors, setErrors] = useState({});
    const [successMessage, setSuccessMessage] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = { email, password };
        try {
            const response = await loginUser(formData);
            if (response.errors) {
                const { non_field_errors } = response.errors;
                setErrors({ msg: non_field_errors });
            } else {
                const { msg, token } = response;
                if (token) {
                    const { access, refresh } = token;
                    Cookies.set('accessToken', access);
                    Cookies.set('refreshToken', refresh);
                    setSuccessMessage(msg);
                    navigate('/');
                }
            }
        } catch (error) {
            console.error(`Login error: ${error}`);
            setErrors({ msg: 'Failed to login. Please try again.' });
        }
    }

    return (
        <div className="log-container">
            <form className="log-form" onSubmit={handleSubmit}>
                <h1>Log In</h1>
                <div className="log-input-group">
                    {/* <i className="fas fa-envelope log-icon"></i> */}
                    <input 
                        type="email" 
                        name="email" 
                        placeholder="Email" 
                        onChange={(e) => setEmail(e.target.value)} 
                        className="log-input"
                    />
                </div>
                <div className="log-input-group">
                    {/* <i className="fas fa-lock log-icon"></i> */}
                    <input 
                        type="password" 
                        name="password" 
                        placeholder="Password" 
                        onChange={(e) => setPassword(e.target.value)} 
                        className="log-input"
                    />
                </div>
                <button type="submit" className="log-button">Login</button>
                <a className="log-link-text" href='/register'>Register</a>
                <br />
                {errors.msg && <p className="log-error-text">{errors.msg}</p>}
                {successMessage && <p className="log-success-text">{successMessage}</p>}
            </form>
        </div>
    );
};

export default Login;
