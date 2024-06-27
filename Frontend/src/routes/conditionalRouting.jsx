import { Routes, Route } from "react-router-dom"
import Register from '../components/Register.jsx';
import Login from '../components/Log-in.jsx';
import Profile from '../components/Profile.jsx';
import Home from '../components/Home.jsx';



function ConditionalRoute() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />} />
        </Routes>
    );
}

export default ConditionalRoute;