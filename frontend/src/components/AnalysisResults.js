import React from 'react';
import { Card, Tab, Tabs, Spinner, Alert } from 'react-bootstrap';
import Summary from './Summary';
import Charts from './Charts';
import DataTable from './DataTable';

const AnalysisResults = ({ data, loading }) => {
  if (loading) {
    return (
      <Card>
        <Card.Body className="text-center">
          <Spinner animation="border" role="status" className="me-2" />
          Analyzing real estate data...
        </Card.Body>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card>
        <Card.Body className="text-center text-muted">
          <h5>Welcome to Real Estate Analysis</h5>
          <p>Enter a query to analyze property data, trends, and market insights.</p>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card>
      <Card.Header>
        <h5 className="mb-0">📊 Analysis Results: {data.query}</h5>
      </Card.Header>
      <Card.Body>
        <Tabs defaultActiveKey="summary" className="mb-3">
          <Tab eventKey="summary" title="📝 Summary">
            <Summary content={data.summary} />
          </Tab>
          <Tab eventKey="charts" title="📈 Charts">
            <Charts data={data.chart_data} />
          </Tab>
          <Tab eventKey="data" title="📋 Data">
            <DataTable data={data.table_data} />
          </Tab>
        </Tabs>
      </Card.Body>
    </Card>
  );
};

export default AnalysisResults;