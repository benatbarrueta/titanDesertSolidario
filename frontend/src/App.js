import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import './App.css';

import Header from './components/Header.js';
import Landing from './components/Landing.js';
import Team from './components/Team.js';
import Challenges from './components/Challenges.js';
import About from './components/About.js';

function App() {
  return (
    <div className="App">
      <Router>
        <Header />
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/team" element={<Team />} />
          <Route path="/about" element={<About />} />
          <Route path="/challenges" element={<Challenges />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
