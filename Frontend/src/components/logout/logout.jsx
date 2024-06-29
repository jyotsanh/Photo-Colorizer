import {Logout} from "../../services/api";
import Cookies from 'js-cookie';


import React, { useEffect , useState } from 'react';

function RemoveToken(){

    const [profile, setProfile] = useState('');
    const [error, setError] = useState('');

    useEffect(()=>{
        const logoutProfile = async () => {
            const refreshToken = Cookies.get('refreshToken');
            const accessToken = Cookies.get('accessToken');
            console.log(`refresh token -- : ${refreshToken}`)
            console.log(`access token -- : ${accessToken}`)
            if (!refreshToken) {
                setError('No refresh token found. Please log in.');
                return;
            }
            try {
                const response = await Logout(refreshToken,accessToken);
                setProfile(response.message);
                Cookies.remove('accessToken');
                Cookies.remove('refreshToken');

            }catch(error){
                setError("token still in there")
            }
        }
        logoutProfile();
    }, []);

    
if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
}
if (profile) {
    return <p>Logout Suceesfully</p>;
}
    return (
        <>

        <h1>Logout</h1>
        </>
    );

}

export default RemoveToken;