import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import "../styles/Challenges.css";
import { apiClient } from "../apiClient";

const Challenges = () => {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    apiClient.getChallenges()
      .then(data => {
        setChallenges(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;

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
        {challenges.map((card, index) => {
          const color = colors[index % colors.length];

          return (
            <NavLink
              key={card.id}
              to={`/challenges/${card.id}`}
              className="challenge-card"
              style={{ borderColor: color }}
            >
              <div className="challenge-card-icon challenge-icon" style={{ color }}>
                {card.icon}
              </div>
              <h2 className="challenge-title">{card.icon} {card.title}</h2>
              <p className="challenge-card-text">{card.options_count} retos</p>

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
