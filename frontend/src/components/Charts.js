import React from 'react';
import { Card, Row, Col } from 'react-bootstrap';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar
} from 'recharts';

const Charts = ({ data }) => {
  if (!data) {
    return <div>No chart data available</div>;
  }

  const locations = Object.keys(data);

  return (
    <Row>
      {locations.map(location => {
        const locationData = data[location];
        const chartData = locationData.years.map((year, index) => ({
          year: year.toString(),
          price: locationData.prices[index],
          demand: locationData.demand[index],
          sales: locationData.sales[index]
        }));

        return (
          <Col md={6} key={location} className="mb-4">
            <Card>
              <Card.Header>
                <h6 className="mb-0">{location}</h6>
              </Card.Header>
              <Card.Body>
                <h6 className="text-center">Price Trends</h6>
                <ResponsiveContainer width="100%" height={200}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="price" 
                      stroke="#8884d8" 
                      name="Avg Price (₹/sqft)"
                    />
                  </LineChart>
                </ResponsiveContainer>

                <h6 className="text-center mt-3">Demand Trends</h6>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar 
                      dataKey="demand" 
                      fill="#82ca9d" 
                      name="Units Sold"
                    />
                  </BarChart>
                </ResponsiveContainer>
              </Card.Body>
            </Card>
          </Col>
        );
      })}
    </Row>
  );
};

export default Charts;