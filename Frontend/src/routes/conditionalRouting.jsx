import { Routes, Route } from "react-router-dom"
import Register from '../components/Register.jsx';
import Login from '../components/Log-in.jsx';
import Home from '../components/Home.jsx';
import About from "../components/AboutUs/about.jsx"
import ContactUs from "../components/contact/contactUs.jsx"
import Profile  from "../components/profile/profile.jsx";
import RemoveToken from "../components/logout/logout.jsx"

function ConditionalRoute() {
    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/about" element={<About />} />
            <Route path="/contact" element={<ContactUs />} />
            <Route path="/logout" element={<RemoveToken />} />
        </Routes>
    );
}

export default ConditionalRoute;