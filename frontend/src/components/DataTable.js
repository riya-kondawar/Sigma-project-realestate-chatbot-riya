import React, { useState } from 'react';
import { Card, Table, Button, Form, Row, Col } from 'react-bootstrap';

const DataTable = ({ data }) => {
  const [filterLocation, setFilterLocation] = useState('');
  const [filterYear, setFilterYear] = useState('');

  const filteredData = data.filter(item => {
    return (
      (!filterLocation || item.final_location === filterLocation) &&
      (!filterYear || item.year.toString() === filterYear)
    );
  });

  const locations = [...new Set(data.map(item => item.final_location))];
  const years = [...new Set(data.map(item => item.year.toString()))];

  const downloadData = () => {
    const csvContent = [
      Object.keys(data[0]).join(','),
      ...filteredData.map(row => 
        Object.values(row).map(value => 
          typeof value === 'string' ? `"${value}"` : value
        ).join(',')
      )
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'real_estate_data.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  };

  if (!data || data.length === 0) {
    return <div>No data available</div>;
  }

  return (
    <Card>
      <Card.Header>
        <Row className="align-items-center">
          <Col>
            <h6 className="mb-0">Real Estate Data</h6>
          </Col>
          <Col xs="auto">
            <Button variant="success" size="sm" onClick={downloadData}>
              📥 Download CSV
            </Button>
          </Col>
        </Row>
      </Card.Header>
      <Card.Body>
        <Row className="mb-3">
          <Col md={6}>
            <Form.Select
              value={filterLocation}
              onChange={(e) => setFilterLocation(e.target.value)}
            >
              <option value="">All Locations</option>
              {locations.map(location => (
                <option key={location} value={location}>
                  {location}
                </option>
              ))}
            </Form.Select>
          </Col>
          <Col md={6}>
            <Form.Select
              value={filterYear}
              onChange={(e) => setFilterYear(e.target.value)}
            >
              <option value="">All Years</option>
              {years.map(year => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </Form.Select>
          </Col>
        </Row>

        <div style={{ maxHeight: '500px', overflow: 'auto' }}>
          <Table striped bordered hover responsive>
            <thead>
              <tr>
                <th>Location</th>
                <th>Year</th>
                <th>Avg Price (₹/sqft)</th>
                <th>Units Sold</th>
                <th>Total Sales (₹)</th>
                <th>Total Area (sqft)</th>
              </tr>
            </thead>
            <tbody>
              {filteredData.map((item, index) => (
                <tr key={index}>
                  <td>{item.final_location}</td>
                  <td>{item.year}</td>
                  <td>₹{item.flat_weighted_avg_rate?.toLocaleString()}</td>
                  <td>{item.total_sold_igr?.toLocaleString()}</td>
                  <td>₹{(item.total_sales_igr / 1000000)?.toFixed(2)}M</td>
                  <td>{item.total_carpet_area?.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </div>
      </Card.Body>
    </Card>
  );
};

export default DataTable;