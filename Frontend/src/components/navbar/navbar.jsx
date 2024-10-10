import React from "react";
import { useNavigate } from 'react-router-dom';
import "./navbar.css";
import Temple from '../../assets/loog.png';

function NavBar() {
    const navigate = useNavigate();
    return (
        <div className="navbar">
            <div className="logo-container">
                <img src={Temple} alt="Logo" />
            </div>
            <div className="links-container">
                <p onClick={() => navigate("/")}>Home</p>
                <p onClick={() => navigate("/about")}>About Us</p>
                <p onClick={() => navigate("/login")}>Log In</p>
            </div>
        </div>
    );
}

export default NavBar;
