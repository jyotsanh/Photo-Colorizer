import React from "react"
import { useNavigate } from 'react-router-dom'
import "./navbar.css"
import Temple from '../../assets/Temple.png'
function NavBar(){
    const navigate = useNavigate();
    return (
        <>
            <div className="navbar">
                <div className="logo-container">
                    <img src={Temple}></img>
                </div>

                <div className="links-container">
                    <p onClick={() => navigate("/")}> Home</p>
                    <p onClick={() => navigate("/about")}> About Us</p>
                    <p onClick={() => navigate("/upload")}> Upload</p>
                    <p onClick={() => navigate("/register")}> Sign Up</p>
                    <p onClick={() => navigate("/login")}> Log-In</p>
                    <p onClick={() => navigate("/profile")}>profile</p>
                    <p onClick={() => navigate("/logout")}>Logout</p>
                    
                </div>
            </div>
        </>
    )
}

export default NavBar;