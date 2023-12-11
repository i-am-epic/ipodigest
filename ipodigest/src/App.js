// src/App.js

import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './components/home';
import DetailPage from './components/DetailPage'; // Import your DetailPage component

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/ipo/:symbol" element={<DetailPage />} />
      </Routes>
    </Router>
  );
};

export default App;
