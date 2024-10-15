import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import "./navbar.css";
import Temple from '../../assets/loog.png';

function NavBar() {
    const [isOpen, setIsOpen] = useState(false);  // State for the hamburger menu
    const navigate = useNavigate();

    const toggleMenu = () => {
        setIsOpen(!isOpen);  // Toggle the menu visibility
    };

    return (
        <div className="navbar">
            <div className="logo-container">
                <img src={Temple} alt="Logo" />
            </div>

            {/* Hamburger icon */}
            <div className={`hamburger ${isOpen ? "open" : ""}`} onClick={toggleMenu}>
                <span className="bar"></span>
                <span className="bar"></span>
                <span className="bar"></span>
            </div>

            {/* Links Container */}
            <div className={`links-container ${isOpen ? "open" : ""}`}>
                <p onClick={() => navigate("/")}>Home</p>
                <p onClick={() => navigate("/about")}>About Us</p>
                <p onClick={() => navigate("/login")}>Log In</p>
            </div>
        </div>
    );
}

export default NavBar;
