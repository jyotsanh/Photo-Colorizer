// src/services/api.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

export const registerUser = async (userData) => {
  const response = await axios.post(`${API_URL}/register`, userData);
  return response.data;
};

export const loginUser = async (userData) => {
  const response = await axios.post(`${API_URL}/login`, userData);
  return response.data;
};

export const Logout = async (refreshToken,accessToken)=>{
  try{
    const response = await axios.post(`${API_URL}/logout`,
      { refresh: refreshToken },
      { headers: {
        Authorization: `Bearer ${accessToken}`,
          },
      }
    )
    return response.data
}catch(error){
  console.error('Logout error:', error);
  throw error;
}
  }

export const getProfile = async (accessToken) => {
  console.log("i AM")
  const response = await axios.get(`${API_URL}/profile`, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });
  return response.data;
};
