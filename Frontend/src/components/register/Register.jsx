import React, { useState } from 'react';
import { registerUser } from '../../services/api';
import Cookies from 'js-cookie';
import './register.css'; // Reusing the login styles

function Register() {
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');
    const [first_name, setFirstName] = useState('');
    const [last_name, setLastName] = useState('');
    const [password, setPassword] = useState('');
    const [password2, setPassword2] = useState('');
    const [successMessage, setSuccessMessage] = useState('');
    const [errors, setErrors] = useState({});

    const handleSubmit = async (e) => {
        e.preventDefault();
        setErrors({});
        const formData = { email, username, first_name, last_name, password, password2 };

        try {
            const response = await registerUser(formData);
            const { msg, token } = response;
            setSuccessMessage(msg);

            if (token) {
                const { access, refresh } = token;
                Cookies.set('accessToken', access);
                Cookies.set('refreshToken', refresh);
            }
        } catch (error) {
            const { data } = error.response;
            const { email, username, non_field_errors } = data.errors;
            setErrors({ email, username, password: non_field_errors });
        }
    };

    return (
        <div className="log-container">
            <form className="form log-form" onSubmit={handleSubmit}>
                <div className="title">
                    Welcome,<br />
                    <span>create your account</span>
                </div>

                {/* Email Input */}
                <input
                    className="input"
                    name="email"
                    placeholder="Email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                {errors.email && <p className="log-error-text">{errors.email}</p>}

                {/* Username Input */}
                <input
                    className="input"
                    name="username"
                    placeholder="Username"
                    type="text"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    required
                />
                {errors.username && <p className="log-error-text">{errors.username}</p>}

                {/* First Name Input */}
                <input
                    className="input"
                    name="first_name"
                    placeholder="First Name"
                    type="text"
                    value={first_name}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                />

                {/* Last Name Input */}
                <input
                    className="input"
                    name="last_name"
                    placeholder="Last Name"
                    type="text"
                    value={last_name}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                />

                {/* Password Input */}
                <input
                    className="input"
                    name="password"
                    placeholder="Password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />

                {/* Confirm Password Input */}
                <input
                    className="input"
                    name="password2"
                    placeholder="Confirm Password"
                    type="password"
                    value={password2}
                    onChange={(e) => setPassword2(e.target.value)}
                    required
                />
                {errors.password && <p className="log-error-text">{errors.password}</p>}
                
                {/* Success Message */}
                {successMessage && <p className="log-success-text">{successMessage}</p>}

                {/* Submit Button */}
                <div className="button-group">
                    <button type="submit" className="button-confirm">Sign Up →</button>
                    <a href="/login" className="button-confirm link-button">Log In →</a>
                </div>
            </form>
        </div>
    );
}

export default Register;
