import React, { useState } from 'react';
import axios from 'axios';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const onFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const onFileUpload = async () => {
        if (!file) {
            alert('Please select a file first!');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        setLoading(true);
        setResponse(null);

        try {
            const res = await axios.post('http://127.0.0.1:5000/upload', formData);
            setResponse(res.data);
        } catch (error) {
            console.error("Upload Error:", error.response || error.message);
            alert(error.response?.data?.error || 'Error uploading file. Please try again.');
        }

        setLoading(false);
    };

    return (
        <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
            <h2>Upload an Image for OCR</h2>
            <input type="file" onChange={onFileChange} />
            <button onClick={onFileUpload} disabled={loading}>
                {loading ? 'Uploading...' : 'Upload'}
            </button>

            {response && (
                <div>
                    {response.error ? (
                        <p style={{ color: 'red' }}>{response.error}</p>
                    ) : (
                        <div>
                            <h3>Matched Medicines:</h3>
                            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px' }}>
                                {Array.isArray(response.matches) && response.matches.length > 0 ? (
                                    response.matches.map((medicine, index) => (
                                        <div
                                            key={index}
                                            style={{
                                                backgroundColor: 'white', // Solid white background
                                                border: '1px solid #ccc',
                                                padding: '16px',
                                                borderRadius: '8px',
                                                width: '200px',
                                                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', // Subtle shadow for elevation
                                                color: '#333', // Dark text for better readability
                                            }}
                                        >
                                            <p><strong>Name:</strong> {medicine["Medicine Name"]}</p>
                                            <p><strong>Composition:</strong> {medicine.Composition}</p>
                                            <p><strong>Uses:</strong> {medicine.Uses}</p>
                                            <p><strong>Manufacturer:</strong> {medicine.Manufacturer}</p>
                                            {medicine["Image URL"] && (
                                                <img
                                                    src={medicine["Image URL"]}
                                                    alt="Medicine"
                                                    style={{ maxWidth: '100%', borderRadius: '4px' }}
                                                />
                                            )}
                                        </div>
                                    ))
                                ) : (
                                    <p>No matches found.</p>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default FileUpload;
