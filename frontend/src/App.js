import React, { useState } from 'react';
import { Container, Row, Col, Navbar, Alert } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import ChatInterface from './components/ChatInterface';
import AnalysisResults from './components/AnalysisResults';
import FileUpload from './components/FileUpload';
import './App.css';

function App() {
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalysis = async (query) => {
    setLoading(true);
    setError('');
    
    try {
      const response = await fetch('/api/analyze/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setAnalysisData(data);
    } catch (err) {
      setError('Failed to analyze data. Please try again.');
      console.error('Analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Navbar bg="dark" variant="dark" className="mb-4">
        <Container>
          <Navbar.Brand>
            🏠 Real Estate Analysis Chatbot
          </Navbar.Brand>
        </Container>
      </Navbar>

      <Container>
        {error && (
          <Alert variant="danger" dismissible onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        <Row>
          <Col lg={4}>
            <FileUpload />
            <ChatInterface 
              onAnalyze={handleAnalysis} 
              loading={loading}
            />
          </Col>
          <Col lg={8}>
            <AnalysisResults 
              data={analysisData} 
              loading={loading}
            />
          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;