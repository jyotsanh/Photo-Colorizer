import './home.css';
import React, { useState } from 'react';
import axios from 'axios';
import { FaUpload, FaDownload } from 'react-icons/fa';
import image from '../../assets/images.png';

function Home() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [originalImage, setOriginalImage] = useState(null);
    const [artisticImage, setArtisticImage] = useState(null);
    const [fineTunedImage, setFineTunedImage] = useState(null);
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
                }
            });

            // Extract Base64 strings from the response data
            const { artistic_image_base64, fine_tuned_image_base64 } = response.data;

            // Set the Base64 strings as image sources
            setOriginalImage(URL.createObjectURL(selectedFile));
            setArtisticImage(artistic_image_base64); // Use the Base64 directly in the `src`
            setFineTunedImage(fine_tuned_image_base64); // Use the Base64 directly in the `src`

        } catch (error) {
            console.error('Error uploading image:', error);
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = () => {
        if (fineTunedImage) {
            const link = document.createElement('a');
            link.href = fineTunedImage;
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
                {/* Row with Uploaded and Pre-Trained Image */}
                <div className="image-row">
                    <div className="image-part">
                        <h3>Uploaded Image</h3>
                        {originalImage && <img src={originalImage} alt="Original" className="image" />}
                    </div>
                    <div className="image-part">
                        <h3>Pre-Trained Colored Image</h3>
                        {loading && <p className="loading-message">Processing image, please wait...</p>}
                        {artisticImage && !loading && <img src={artisticImage} alt="Colored" className="image" />}
                    </div>
                </div>
                {/* Centered Fine-Tuned Image */}
                <div className="image-part">
                    <h3>Fine-Tuned Colored Image</h3>
                    {loading && <p className="loading-message">Processing image, please wait...</p>}
                    {fineTunedImage && !loading && <img src={fineTunedImage} alt="Fine-Tuned Colored" className="image" />}
                </div>
            </div>

            <div className="upload-section">
                <input type="file" onChange={handleFileChange} className="file-input" />
            </div>

            <div className="buttons-container">
                <button onClick={handleUpload} className="upload-photo-button" disabled={loading}>
                    <FaUpload />
                    Upload Photo
                </button>
                <button onClick={handleDownload} className="download-button" disabled={!fineTunedImage}>
                    <FaDownload />
                    Download Image
                </button>
            </div>

            <section className="heritage-section">
                <h2>Temple Heritage</h2>
                <div className="heritage-content">
                    <img src={image} alt="Temple" className="heritage-image" />
                    <div className="heritage-description">
                        <h3>The Legacy of Ancient Architecture</h3>
                        <p>
                            Experience the grandeur and spiritual serenity of ancient temple architecture that has 
                            stood the test of time. These structures are not just places of worship but are 
                            masterpieces that showcase the dedication and artistry of our ancestors.
                        </p>
                    </div>
                </div>
            </section>
        </div>
    );
}

export default Home;
