import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import './FileUpload.css';  // Make sure to create this CSS file

function FileUpload() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [results, setResults] = useState([]);

  const onDrop = useCallback(acceptedFiles => {
    setSelectedFiles(acceptedFiles);
  }, []);

  const onFileUpload = async () => {
    const formData = new FormData();
    if (selectedFiles) {
      for (let i = 0; i < selectedFiles.length; i++) {
        formData.append('files[]', selectedFiles[i]);
      }
      try {
        const response = await axios.post('http://localhost:5000/upload', formData);
        setResults(response.data.results);
      } catch (error) {
        console.error('There was an error uploading the files!', error);
        alert('There was an error uploading the files. Please check the console for more details.');
      }
    }
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop, accept: '.pdf' });

  return (
    <div className="file-upload-container">
      <h2>Resume Screener</h2>
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here ...</p>
        ) : (
          <p>Drag 'n' drop some files here, or click to select files</p>
        )}
      </div>
      <button onClick={onFileUpload} className="upload-button">Upload Files</button>
      <div>
        {results.length > 0 && (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
  <tbody>
      <h4 style = { { textAlign: 'left'}}> Results </h4>

    {results.map((result, index) => (
      <tr key={index}>
        <td style={{ border: '1px solid transparent', textAlign: 'justify', padding: '8px', fontSize: '15px' }}>
          {result}
        </td>
      </tr>
    ))}
  </tbody>
</table>

        )}
      </div>
    </div>
  );
}

export default FileUpload;
