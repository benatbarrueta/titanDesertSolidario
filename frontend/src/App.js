import React from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';

import './App.css';

import Header from './components/Header.js';
import Landing from './components/Landing.js';
import Team from './components/Team.js';
import Challenges from './components/Challenges.js';
import About from './components/About.js';
import ChallengeDetail from './components/ChallengeDetail';

import AdminRoute from './admin/auth/AdminRoute';
import AdminLogin from './admin/auth/AdminLogin';
import AdminAuthCallback from './admin/auth/AdminAuthCallback';
import AdminDashboard from './admin/pages/AdminDashboard';
import AdminStages from './admin/pages/AdminStages';
import AdminChallenges from './admin/pages/AdminChallenges';
import AdminParticipations from './admin/pages/AdminParticipations';
import AdminWarriors from './admin/pages/AdminWarriors';

import { AdminAuthProvider } from './admin/auth/AdminAuthContext';

function AppLayout() {
  const location = useLocation();
  const isAdminRoute = location.pathname.startsWith('/admin');

  return (
    <>
      {!isAdminRoute && <Header />}

      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/team" element={<Team />} />
        <Route path="/about" element={<About />} />
        <Route path="/challenges" element={<Challenges />} />
        <Route path="/challenges/:challengeId" element={<ChallengeDetail />} />

        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin/auth/callback" element={<AdminAuthCallback />} />

        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminDashboard />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/stages"
          element={
            <AdminRoute>
              <AdminStages />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/challenges"
          element={
            <AdminRoute>
              <AdminChallenges />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/participations"
          element={
            <AdminRoute>
              <AdminParticipations />
            </AdminRoute>
          }
        />
        <Route
          path="/admin/warriors"
          element={
            <AdminRoute>
              <AdminWarriors />
            </AdminRoute>
          }
        />
      </Routes>
    </>
  );
}

function App() {
  return (
    <div className="App">
      <AdminAuthProvider>
        <Router>
          <AppLayout />
        </Router>
      </AdminAuthProvider>
    </div>
  );
}

export default App;