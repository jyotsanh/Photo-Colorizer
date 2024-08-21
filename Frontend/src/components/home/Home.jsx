import "./home.css";
import React, { useState } from 'react';
import axios from 'axios';
import { FaUpload, FaDownload } from 'react-icons/fa';
import image from '../../assets/image.png'
function Home() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [originalImage, setOriginalImage] = useState(null);
    const [coloredImage, setColoredImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            setError('Please select an image first');
            return;
        }

        const formData = new FormData();
        formData.append('image', selectedFile);

        setLoading(true);
        setError(null);

        try {
            const response = await axios.post('http://localhost:8000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                responseType: 'blob'
            });

            const coloredImageBlob = new Blob([response.data], { type: 'image/jpeg' });
            const coloredImageUrl = URL.createObjectURL(coloredImageBlob);

            setOriginalImage(URL.createObjectURL(selectedFile));
            setColoredImage(coloredImageUrl);
        } catch (error) {
            console.error('Error uploading image:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = () => {
        if (coloredImage) {
            const link = document.createElement('a');
            link.href = coloredImage;
            link.download = 'colored-image.jpg';
            link.click();
        }
    };

    return (
        <div className="container">
            <header className="header">
                <h1>Welcome to Temple Vision</h1>
            </header>

            <div className="image-section">
                <div className="image-parts">
                    <div className="image-part">
                        <h3>Uploaded Image</h3>
                        {originalImage && <img src={originalImage} alt="Original" className="image" />}
                    </div>
                    <div className="image-part">
                        <h3>Colored Image</h3>
                        {loading && <p className="loading-message">Processing image, please wait...</p>}
                        {coloredImage && !loading && <img src={coloredImage} alt="Colored" className="image" />}
                    </div>
                </div>
            </div>


            {/* If u cannot uplaod from that then onlu uncomment this one */}
            
            <div className="upload-section">
                <input type="file" onChange={handleFileChange} className="file-input" />
            </div>

                    {/* First try to uplaod the image with this uplaod button  */}

            <div className="buttons-container">
                <button onClick={handleUpload} className="upload-photo-button" disabled={loading}>
                    <FaUpload className="icon" /> {loading ? 'Processing...' : 'Upload Photo'}
                </button>
                <button onClick={handleDownload} className="download-button" disabled={!coloredImage}>
                    <FaDownload className="icon" /> Download
                </button>
            </div>

            <div className="heritage-section">
                <h2>See Our Heritage in its Glories Form By Coloring the Past History</h2>
                <div className="heritage-content">
                    <img src={image} alt="Heritage" className="heritage-image" />
                    <div className="heritage-description">
                        <h3>Change the Image of the History Full of Color.</h3>
                        <p>We change the black and white image into a color image using AI deoldify.</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Home;
