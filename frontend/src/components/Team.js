import React, { useEffect, useMemo, useState } from 'react';
import '../styles/Team.css';
import { apiClient } from '../apiClient';

const BACKEND_BASE_URL =
  process.env.REACT_APP_BACKEND_BASE_URL || "http://localhost:8000";

const buildPhotoUrl = (photoUrl) => {
  if (!photoUrl) return null;

  if (photoUrl.startsWith("http://") || photoUrl.startsWith("https://")) {
    return photoUrl;
  }

  return `${BACKEND_BASE_URL}${photoUrl}`;
};

const formatEUR = (value) => {
  const n = Number(value ?? 0);
  return n.toLocaleString('es-ES', { style: 'currency', currency: 'EUR' });
};

const Team = () => {
  const [warriors, setWarriors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const sortedWarriors = useMemo(() => {
    return [...warriors].sort((a, b) => (a.dorsal ?? 0) - (b.dorsal ?? 0));
  }, [warriors]);

  useEffect(() => {
    window.scrollTo(0, 0);
    setLoading(true);
    setError(null);

    apiClient
      .getWarriors()
      .then((data) => {
        setWarriors(Array.isArray(data) ? data : []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || 'Error cargando el equipo');
        setLoading(false);
      });
  }, []);

  if (loading) return <p className="team-status">Cargando...</p>;
  if (error) return <p className="team-status">Error: {error}</p>;

  return (
    <div className="team-page">
      <h1 className="team-title">NUESTROS {sortedWarriors.length} GUERREROS</h1>

      {sortedWarriors.length === 0 ? (
        <div className="team-empty">
          <p>No hay guerreros disponibles todavía.</p>
        </div>
      ) : (
        <div className="team-grid">
          {sortedWarriors.map((w) => {

            const photoUrl = buildPhotoUrl(w.photo_url);

            return (
              <article key={w.id} className="warrior-card">
                <div className="warrior-top">

                  {/* FOTO */}
                  {photoUrl && (
                    <img
                      src={photoUrl}
                      alt={w.name}
                      className="warrior-photo"
                    />
                  )}

                  {/* DORSAL */}
                  <div className="warrior-dorsal">#{w.dorsal}</div>

                </div>

                <div className="warrior-bottom">
                  <div className="warrior-name">{w.name}</div>

                  <div className="warrior-raise">
                    <div className="warrior-label">Recaudado</div>
                    <div className="warrior-amount">{formatEUR(w.raised)}</div>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default Team;