// src/components/Login.js
import React, { useState } from 'react';
import { loginUser } from '../services/api';
import { useNavigate } from 'react-router-dom';

import Cookies from 'js-cookie';
function Login(){
    const [email,setEmail] = useState('');
    const [password,setPassword] = useState('');
    const [errors,setErrors] = useState({});
    const [successMessage,setSuccessMessage] = useState('');
    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        // set the formdata which we will send throguh axios
        e.preventDefault();
        const formdata = {
            email:email,
            password:password
        } 
        // remove all the previous  errors and success messages
        setErrors('')
        setSuccessMessage('')
        
        try{
            console.log(formdata)
            const response = await loginUser(formdata);
            const {errors} = response // check if the response has any errors 
            if(errors){
                const {non_field_errors} = errors //take out the non_field_errors
                setErrors({msg:non_field_errors}) // include it to setErrors
            }else{
                console.log("response : ")
                console.log(response)

                const {msg,token} = response
                
                if (token) {
                    const { access, refresh } = token; //-> token fetched

                    
                    // remove the previous tokens
                    Cookies.remove('accessToken');
                    Cookies.remove('refreshToken');
                    // Store the tokens in cookies
                    Cookies.set('accessToken', access);
                    Cookies.set('refreshToken', refresh);
                    setSuccessMessage(msg); // set the sucessfull message
                    navigate('/'); // go to home page
                }
            }
        }catch(error){
            console.log(`error:  ${error }`)
            
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <input 
            type="email" 
            name="email" 
            placeholder="Email" 
            onChange={(e)=>setEmail(e.target.value)} 
            />


            <input 
            type="password" 
            name="password" 
            placeholder="Password" 
            onChange={(e)=>setPassword(e.target.value)} 
            />

            <button type="submit">Login</button>
            <a className="link-text" href='/register'>Register</a>
            <br />
            {errors.msg && <p className="error-text">{errors.msg}</p>}
            {successMessage && <p className="success-text">{successMessage}</p>}
        </form>
    );
};

export default Login;
