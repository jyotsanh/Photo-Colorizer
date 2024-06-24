// src/components/Profile.js
import React, { useEffect, useState } from 'react';
import { getProfile } from '../services/api';

const Profile = ({ accessToken }) => {
    const [profile, setProfile] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await getProfile(accessToken);
                setProfile(response);
            } catch (error) {
                console.error('Error fetching profile', error);
            }
        };

        fetchProfile();
    }, [accessToken]);

    if (!profile) return <div>Loading...</div>;

    return (
        <div>
            <h2>Profile</h2>
            <pre>{JSON.stringify(profile, null, 2)}</pre>
        </div>
    );
};

export default Profile;
