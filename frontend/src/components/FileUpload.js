import React, { useState } from 'react';
import { Card, Form, Button, Alert, Spinner } from 'react-bootstrap';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setMessage('');
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage('Please select a file first');
      return;
    }

    setUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload/', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      setMessage('File uploaded and data processed successfully!');
      setFile(null);
      // Clear file input
      document.getElementById('file-input').value = '';
    } catch (error) {
      setMessage('Upload failed. Please try again.');
      console.error('Upload error:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Card className="mb-4">
      <Card.Header>
        <h6 className="mb-0">📁 Upload Excel Data</h6>
      </Card.Header>
      <Card.Body>
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Select Excel file:</Form.Label>
            <Form.Control
              id="file-input"
              type="file"
              accept=".xlsx,.xls"
              onChange={handleFileChange}
              disabled={uploading}
            />
          </Form.Group>
          
          <Button
            variant="primary"
            onClick={handleUpload}
            disabled={uploading || !file}
            className="w-100"
          >
            {uploading ? (
              <>
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                  className="me-2"
                />
                Uploading...
              </>
            ) : (
              'Upload Data'
            )}
          </Button>
        </Form>

        {message && (
          <Alert 
            variant={message.includes('failed') ? 'danger' : 'success'} 
            className="mt-3 small"
          >
            {message}
          </Alert>
        )}
      </Card.Body>
    </Card>
  );
};

export default FileUpload;