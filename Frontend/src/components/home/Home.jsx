import "./home.css";
import React, { useState } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';

function Home(){
    const [selectedFile, setSelectedFile] = useState(null);
    const [originalImage, setOriginalImage] = useState(null);
    const [bwImage, setBwImage] = useState(null);
    const [loading, setLoading] = useState(false);  // Loading state
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('image', selectedFile);

        if (selectedFile === null) {
            setError('Please select an image first');
            return;
        }

        setLoading(true);  // Start loading
        setError(null);  // Clear previous errors

        try {
            const response = await axios.post('http://localhost:8000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                    // 'Authorization': `Bearer ${Cookies.get('accessToken')}`
                },
                responseType: 'blob'
            });

            const bwImageBlob = new Blob([response.data], { type: 'image/jpeg' });
            const bwImageUrl = URL.createObjectURL(bwImageBlob);

            setOriginalImage(URL.createObjectURL(selectedFile));
            setBwImage(bwImageUrl);
        } catch (error) {
            console.error('Error uploading image:', error);
            setError(error.message);
        } finally {
            setLoading(false);  // End loading
        }
    };

    return (
        <div className="container">
            <header className="header">
                <h1>Welcome to Temple Vision</h1>
            </header>
            <div className="upload-section">
                <input type="file" onChange={handleFileChange} className="file-input" />
                <button onClick={handleUpload} className="upload-button" disabled={loading}>
                    {loading ? 'Processing...' : 'Upload'}
                </button>
                {error && <p className="error-message">{error}</p>}
            </div>
            <div className="image-section">
                {loading && <p className="loading-message">Processing image, please wait...</p>} {/* Loading message */}
                {!loading && originalImage && (
                    <div className="image-container">
                        <h3>Original Image</h3>
                        <img src={originalImage} alt="Original" className="image" />
                    </div>
                )}
                {!loading && bwImage && (
                    <div className="image-container">
                        <h3>Colored Image</h3>
                        <img src={bwImage} alt="Colored" className="image" />
                    </div>
                )}
            </div>
        </div>
    );
}

export default Home;
