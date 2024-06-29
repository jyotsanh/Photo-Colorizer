import { Route, Routes } from "react-router-dom";
import Home from "../src/components/Home";
import About from '../src/components/AboutUs/about.jsx'
import SignUp from "../src/components/Register";
import SignIn from "../src/components/Log-in";
import Contact from "../src/components/contact/contactUs.jsx";
import Profile from "../src/components/Profile.jsx";

function ConditionalRoute() {


    return (
    <>
        <Routes>
            <Route path='/register' element={<SignUp />} />
            <Route path='/profile' element={<Profile />} />
            <Route path='/login' element={<SignIn />} />
            <Route path='/' element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path='/contact' element={<Contact />} />
        </Routes>
    </>
    );

}

export default ConditionalRoute;

