// src/components/HomePage.js

import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Table, TableContainer, TableHead, TableBody, TableRow, TableCell, Paper } from '@mui/material';

const HomePage = () => {
    const [ipoData, setIPOData] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // Replace 'http://localhost:8000/ipo/api/ipoData/' with your Django API endpoint
                const response = await fetch('http://localhost:8000/ipo/api/ipoData/');
                const data = await response.json();
                setIPOData(data);
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, []);

    return (
        <div style={{ padding: '20px' }}>
            <h1>Welcome to the IPO Screener</h1>

            <TableContainer component={Paper} style={{ borderRadius: '15px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)' }}>
                <Table>
                    <TableHead style={{ backgroundColor: '#2196f3', borderRadius: '15px' }}>
                        <TableRow>
                            {/* ... (header cells) */}
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {ipoData.map((ipo) => (
                            <TableRow key={ipo.symbol}>
                                <TableCell>{ipo.slNumber}</TableCell>
                                <TableCell>
                                    <img src={ipo.logo} alt={`${ipo.name} Logo`} style={{ width: '50px', borderRadius: '50%' }} />
                                </TableCell>
                                {/* ... (other cells) */}
                                <TableCell>
                                    {/* Use Link component with a valid wrapper (e.g., a div or a TableCell) */}
                                    <Link to={`/ipo/${ipo.symbol}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                                        View Details
                                    </Link>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </div>
    );
};

export default HomePage;
