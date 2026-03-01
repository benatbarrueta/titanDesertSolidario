import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/Header.css';

const Header = () => {

  const [isOpen, setIsOpen] = useState(false);

  const closeMenu = () => setIsOpen(false);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
      document.documentElement.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
      document.documentElement.style.overflow = "";
    }

    return () => {
      document.body.style.overflow = "";
      document.documentElement.style.overflow = "";
    };
  }, [isOpen]);

  return (
    <header>
      <h1>TITAN DESERT SOLIDARIO</h1>

      {/* Desktop Nav */}
      <div className="nav-links">
        <NavLink to="/" onClick={closeMenu} className={({ isActive }) => (isActive ? 'active' : '')}>Inicio</NavLink>
        <NavLink to="/team" onClick={closeMenu} className={({ isActive }) => (isActive ? 'active' : '')}>Equipo</NavLink>
        <NavLink to="/challenges" onClick={closeMenu} className={({ isActive }) => (isActive ? 'active' : '')}>Retos</NavLink>
        <NavLink to="/about" onClick={closeMenu} className={({ isActive }) => (isActive ? 'active' : '')}>La Causa</NavLink>
      </div>

      {/* Hamburger button */}
      <button 
        className={`hamburger ${isOpen ? "open" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* Mobile Drawer */}
      {isOpen && <div className="menu-overlay" onClick={closeMenu}></div>}
      <div className={`mobile-menu ${isOpen ? "open" : ""}`}>
        <NavLink 
          to="/" 
          onClick={closeMenu}
          className={({ isActive }) => isActive ? "active" : ""}
          >
            Inicio
        </NavLink>

        <NavLink 
          to="/team" 
          onClick={closeMenu}
          className={({ isActive }) => isActive ? "active" : ""}
        >
          Equipo
        </NavLink>

        <NavLink 
          to="/challenges" 
          onClick={closeMenu}
          className={({ isActive }) => isActive ? "active" : ""}
        >
          Retos
        </NavLink>

        <NavLink 
          to="/about" 
          onClick={closeMenu}
          className={({ isActive }) => isActive ? "active" : ""}
        >
          La Causa
        </NavLink>
      </div>

    </header>
  );
};

export default Header;