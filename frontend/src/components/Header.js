import React from 'react';
import {NavLink} from 'react-router-dom';

import '../styles/Header.css';

const Header = () => {
  return (
    <header>
      <h1>TITAN DESERT SOLIDARIO</h1>

      <div className="nav-links">
        <NavLink to="/" className={({ isActive }) => (isActive ? 'active' : '')}>Inicio</NavLink>
        <NavLink to="/team" className={({ isActive }) => (isActive ? 'active' : '')}>Equipo</NavLink>
        <NavLink to="/challenges" className={({ isActive }) => (isActive ? 'active' : '')}>Retos</NavLink>
        <NavLink to="/about" className={({ isActive }) => (isActive ? 'active' : '')}>La Causa</NavLink>
      </div>
    </header>
  );
};

export default Header;