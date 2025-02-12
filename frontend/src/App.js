import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/test')
      .then(response => setMessage(response.data.message))
      .catch(error => {
        console.error('Error fetching test message:', error);
        setMessage('Failed to fetch test message');
      });
  }, []);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log(response.data);
      alert(response.data.message);
    } catch (error) {
      console.error('Error uploading file:', error);
      let errorMessage = 'Error uploading file'; // Default error message
      if (error.response && error.response.data && error.response.data.error) {
        // If the server sends a specific error message, display it
        errorMessage = error.response.data.error;
      }
      alert(errorMessage);
    }
  };

  return (
    <div className="App">
      <h1>Document Upload</h1>
      <p>{message}</p>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
    </div>
  );
}

export default App;
