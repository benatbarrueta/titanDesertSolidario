import React, { useEffect, useState } from 'react';
import '../styles/Team.css';
import { apiClient } from '../apiClient';

const Team = () => {
  const [warriors, setWarriors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    window.scrollTo(0, 0);
    apiClient.getWarriors()
      .then(data => {
        setWarriors(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div className="team-page">
      <h1 className="team-title">NUESTROS 25 GUERREROS</h1>

      <div className="team-grid">
        {warriors.map((w) => (
          <article key={w.id} className="warrior-card">
            <div className="warrior-top">
              <div className="warrior-dorsal">#{w.dorsal}</div>
            </div>

            <div className="warrior-bottom">
              <div className="warrior-name">{w.name}</div>
              <div className="warrior-label">Recaudado</div>
              <div className="warrior-amount">€{w.raised}</div>
            </div>
          </article>
        ))}
      </div>
    </div>
  );
};

export default Team;
