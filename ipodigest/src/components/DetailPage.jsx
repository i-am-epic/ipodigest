// src/components/DetailPage.js

import React from 'react';

const DetailPage = ({ match }) => {
    const { symbol } = match.params;

    return (
        <div>
            <h2>Details for IPO with Symbol: {symbol}</h2>
            {/* Add additional details or components as needed */}
        </div>
    );
};

export default DetailPage;
