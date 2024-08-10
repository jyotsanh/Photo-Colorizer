import React, { useEffect, useState } from 'react';
import {getProfile} from '../../services/api';
import { useNavigate } from 'react-router-dom';

import Cookies from 'js-cookie';
const Profile =  ()=> {
    const [profile, setProfile] = useState('');
    const [error, setError] = useState('');

    const navigate = useNavigate();


    useEffect(()=>{
        const fetchProfile = async () => {
            const accessToken = Cookies.get('accessToken');
            console.log(`access token : ${accessToken}`)
            if (!accessToken) {
                setError('Please Sign-in/Sign-Up.');
                return;
            }
            try {
                const profileData = await getProfile(accessToken);
                setProfile(profileData);
                console.log("profile data : ")
                console.log(profileData)
            }catch(error){
                navigate('/login')
                console.error('Error fetching profile:', error);
            }
        }
        fetchProfile();
    }, []);
    const handleSignIn = () => {
        navigate('/login'); // For React Router v6
    };

if (error) {
    return (
        <>
        <p style={{ color: 'red' }}>{error}</p>
        <button onClick={handleSignIn}>Sign-In</button>
        </>
    );
}
if (!profile) {
    return (
    <>
    <p>Loading profile...</p>
    <button onClick={handleSignIn}>Sign-In</button>
    </>

    );
}
    return (
        <>
        <div>
            <h1>Profile</h1>
            <p><strong>Email:</strong> {profile.email}</p>
            <p><strong>First Name:</strong> {profile.first_name}</p>
            <p><strong>Last Name:</strong> {profile.last_name}</p>
            <p><strong>Username:</strong> {profile.username}</p>
        </div>
        </>
    );
};

export default Profile;