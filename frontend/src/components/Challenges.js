import React, { useEffect } from "react";
import { NavLink } from "react-router-dom";
import "../styles/Challenges.css";

const Challenges = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const cards = [
    { title: "ORDEN Y POSICIÓN", challengeNumber: 4, icon: "🏁" },
    { title: "TIEMPOS", challengeNumber: 3, icon: "⏱️" },
    { title: "KILÓMETROS", challengeNumber: 3, icon: "📍" },
    { title: "AVERIAS E INCIDENTES", challengeNumber: 3, icon: "🔧" },
    { title: "MOMENTOS VIRALES", challengeNumber: 4, icon: "😅" },
    { title: "MENTAL Y RESISTENCIA", challengeNumber: 3, icon: "🧠" },
    { title: "DUELOS ENTRE CORREDORES", challengeNumber: 3, icon: "👥" },
    { title: "RETOS DE EQUIPO", challengeNumber: 3, icon: "🏜️" },
  ];

  const colors = ["red", "orange", "yellow", "green", "purple", "violet", "hotpink", "cyan"];

  const slugify = (str) =>
    str
      .normalize("NFD")
      .replace(/\p{Diacritic}/gu, "")
      .toLowerCase()
      .trim()
      .replace(/\s+/g, "-")
      .replace(/[^a-z0-9-]/g, "");

  return (
    <div className="challenges">
      <h1 className="challenges-title">ELIGE TU RETO SOLIDARIO</h1>

      <p className="challenges-description">
        Selecciona una categoría de retos. Cada participación desde 5€ va directo a la lucha contra la ELA.
      </p>

      <div className="challenge-cards">
        {cards.map((card, index) => {
          const color = colors[index % colors.length];

          return (
            <NavLink
              key={card.title}
              to={`/challenges/${slugify(card.title)}`}
              className="challenge-card"
              style={{ borderColor: color }}
            >
              {/* Alias: challenge-card-icon (CSS actual) + challenge-icon (por compatibilidad) */}
              <div className="challenge-card-icon challenge-icon">{card.icon}</div>

              {/* Usar clase del CSS */}
              <div className="challenge-card-title">{card.title}</div>

              <div className="challenge-card-text">{card.challengeNumber} retos disponibles</div>

              {/* Alias: challenge-card-price (CSS actual) + challenge-price (por compatibilidad) */}
              <div className="challenge-card-price challenge-price" style={{ color }}>
                Desde €5 →
              </div>
            </NavLink>
          );
        })}
      </div>
    </div>
  );
};

export default Challenges;
