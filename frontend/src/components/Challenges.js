import React from "react";
import { NavLink } from 'react-router-dom';
import { useEffect } from 'react';

import '../styles/Challenges.css'

const Challenges = () => {
  useEffect(() => {
    window.scrollTo(0, 0); // Desplaza la página al inicio al cargar el componente
  }, []);

  const cards = [
        { title: 'ORDEN Y POSICIÓN', challengeNumber: 4, icon: '🏁' },
        { title: 'TIEMPOS', challengeNumber: 3, icon: '⏱️' },
        { title: 'KILÓMETROS', challengeNumber: 3, icon: '📍' },
        { title: 'AVERIAS E INCIDENTES', challengeNumber: 3, icon: '🔧' },
        { title: 'MOMENTOS VIRALES', challengeNumber: 4, icon: '😅' },
        { title: 'MENTAL Y RESISTENCIA', challengeNumber: 3, icon: '🧠' },
        { title: 'DUELOS ENTRE CORREDORES', challengeNumber: 3, icon: '👥' },
        { title: 'RETOS DE EQUIPO', challengeNumber: 3, icon: '🏜️' },
    ];
  const colors = [
    'red', 'orange', 'yellow', 'green', 'purple', 'violet', 'hotpink', 'cyan'
  ];

  const removeAccents = (str) => {
    return str.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase();
  };

  return (
    <div className="challenges">
      <h1 className="challenges-title">ELIGE TU RETO SOLIDARIO</h1>

      <p className="challenges-description">Selecciona una categoría de retos. Cada participación desde 5€ va directo a la lucha contra la ELA.</p>

      <div className="challenge-cards">
        {cards.map((card, index) => (
          <NavLink 
            to={`/challenges/${removeAccents(card.title).replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')}`} /* Ruta dinámica basada en el título */
            key={index} 
            className="challenge-card" 
            style={{ borderColor: colors[index % colors.length] }} /* Color del borde */
          >
            <div className="challenge-icon">{card.icon}</div>
            <h2>{card.icon} {card.title}</h2>
            <p>{card.challengeNumber} retos disponibles</p>
            <p 
              className="challenge-price" 
              style={{ color: colors[index % colors.length] }} /* Color del texto 'Desde €5 →' */
            >
              Desde €5 →
            </p>
          </NavLink>
        ))}
      </div>
    </div>
  );
};

export default Challenges;