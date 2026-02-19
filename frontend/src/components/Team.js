import React, { useMemo, useEffect } from 'react';
import '../styles/Team.css';

const Team = () => {
  // Mock de 25 “guerreros”
  const warriors = useMemo(() => {
    const names = [
      'Ana Martínez', 'Carlos Ruiz', 'Elena López', 'Miguel Sánchez', 'Laura García',
      'David Torres', 'Sofía Jiménez', 'Javier Morales', 'Carmen Vega', 'Roberto Díaz',
      'Paula Romero', 'Álvaro Navarro', 'Lucía Ortega', 'Daniel Castro', 'Marta Rivas',
      'Iván Herrera', 'Nuria Molina', 'Hugo Santos', 'Claudia Ramos', 'Sergio Gil',
      'Irene León', 'Pablo Serra', 'Aitana Cruz', 'Marcos Vidal', 'Noa Fuentes'
    ];

    const dorsalsStart = 101;

    return names.map((name, i) => ({
      id: `${dorsalsStart + i}`,
      dorsal: dorsalsStart + i,
      name,
      raised: 0 // mock
    }));
  }, []);

  useEffect(() => {
          window.scrollTo(0, 0);
      }, []);

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
