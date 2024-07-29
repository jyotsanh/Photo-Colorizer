import "./home.css"

function Home(){
    const [selectedFile, setSelectedFile] = useState(null);
    const [originalImage, setOriginalImage] = useState(null);
    const [bwImage, setBwImage] = useState(null);
    const [error, setError] = useState(null);
    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };
    const handleUpload = async () => {
        const formData = new FormData();
        formData.append('image', selectedFile);
        if(selectedFile === null){
            setError('Please select an image first');
            return
        }
        try {
            const response = await axios.post('http://localhost:8000/api/upload', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            const bwImageBlob = new Blob([response.data.bw_image], { type: 'image/jpeg' });
            const bwImageUrl = URL.createObjectURL(bwImageBlob);

            setOriginalImage(URL.createObjectURL(selectedFile));
            setBwImage(bwImageUrl);
        } catch (error) {
            console.error('Error uploading image:', error);
            setError(error.message);
        }
    };
    return (
        <div className="container">
            <header className="header">
                <h1>Welcome to Temple Vision</h1>
            </header>
            <div className="upload-section">
                <input type="file" onChange={handleFileChange} className="file-input" />
                <button onClick={handleUpload} className="upload-button">Upload</button>
                {error && <p className="error-message">{error}</p>}
            </div>
            <div className="image-section">
                {originalImage && (
                    <div className="image-container">
                        <h3>Original Image:</h3>
                        <img src={originalImage} alt="Original" className="image" />
                    </div>
                )}
                {bwImage && (
                    <div className="image-container">
                        <h3>Black and White Image:</h3>
                        <img src={bwImage} alt="Black and White" className="image" />
                    </div>
                )}
            </div>
        </div>
    );

}

export default Home;