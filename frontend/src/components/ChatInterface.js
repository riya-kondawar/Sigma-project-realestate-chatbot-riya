import React, { useState } from 'react';
import { Card, Form, Button, ListGroup, Spinner } from 'react-bootstrap';

const SAMPLE_QUERIES = [
  "Give me analysis of Wakad",
  "Compare Ambegaon Budruk and Aundh demand trends",
  "Show price growth for Akurdi over the last 3 years",
  "Analyze real estate trends in Pune",
  "Show me data for all locations in 2023"
];

const ChatInterface = ({ onAnalyze, loading }) => {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onAnalyze(query);
    }
  };

  const handleSampleQuery = (sampleQuery) => {
    setQuery(sampleQuery);
    onAnalyze(sampleQuery);
  };

  return (
    <Card className="h-100">
      <Card.Header>
        <h5 className="mb-0">💬 Real Estate Chat</h5>
      </Card.Header>
      <Card.Body className="d-flex flex-column">
        <Form onSubmit={handleSubmit} className="mb-3">
          <Form.Group>
            <Form.Label>Enter your query:</Form.Label>
            <Form.Control
              as="textarea"
              rows={3}
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g., Analyze Wakad property trends..."
              disabled={loading}
            />
          </Form.Group>
          <Button 
            type="submit" 
            variant="primary" 
            className="w-100 mt-2"
            disabled={loading || !query.trim()}
          >
            {loading ? (
              <>
                <Spinner
                  as="span"
                  animation="border"
                  size="sm"
                  role="status"
                  aria-hidden="true"
                  className="me-2"
                />
                Analyzing...
              </>
            ) : (
              'Analyze'
            )}
          </Button>
        </Form>

        <div className="mt-auto">
          <h6>Try these sample queries:</h6>
          <ListGroup>
            {SAMPLE_QUERIES.map((sampleQuery, index) => (
              <ListGroup.Item
                key={index}
                action
                onClick={() => handleSampleQuery(sampleQuery)}
                className="small"
                disabled={loading}
              >
                {sampleQuery}
              </ListGroup.Item>
            ))}
          </ListGroup>
        </div>
      </Card.Body>
    </Card>
  );
};

export default ChatInterface;