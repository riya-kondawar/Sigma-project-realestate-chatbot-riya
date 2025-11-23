import React from 'react';
import { Card } from 'react-bootstrap';
import ReactMarkdown from 'react-markdown';

const Summary = ({ content }) => {
  return (
    <Card>
      <Card.Body>
        <ReactMarkdown>{content}</ReactMarkdown>
      </Card.Body>
    </Card>
  );
};

export default Summary;