import React, { useEffect } from 'react';
import '../styles/About.css';

const About = () => {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

  return (
    <main className="about-page">
      {/* Background + Hero */}
      <section className="about-hero">
        <div className="about-hero-inner">
          <h1 className="about-title">LUCHAMOS CONTRA LA ELA</h1>

          <div className="about-cards">
            {/* Card 1 */}
            <article className="about-card">
              <h2 className="about-card-title about-card-title--accent">¿Qué es la ELA?</h2>
              <p className="about-card-text">
                La Esclerosis Lateral Amiotrófica (ELA) es una enfermedad neurodegenerativa que afecta a las
                neuronas motoras, provocando una pérdida progresiva de la capacidad de movimiento.
                Actualmente no tiene cura.
              </p>
            </article>

            {/* Card 2 */}
            <article className="about-card about-card--left-accent">
              <h2 className="about-card-title">Fundación Dale CandELA</h2>

              <p className="about-card-subtitle">El 100% de los fondos recaudados se destinan a:</p>

              <ul className="about-list">
                <li className="about-list-item">
                  <span className="about-check" aria-hidden="true">✅</span>
                  <span>Investigación científica para encontrar una cura</span>
                </li>
                <li className="about-list-item">
                  <span className="about-check" aria-hidden="true">✅</span>
                  <span>Apoyo directo a familias afectadas</span>
                </li>
                <li className="about-list-item">
                  <span className="about-check" aria-hidden="true">✅</span>
                  <span>Equipamiento médico especializado</span>
                </li>
                <li className="about-list-item">
                  <span className="about-check" aria-hidden="true">✅</span>
                  <span>Terapias y tratamientos de apoyo</span>
                </li>
              </ul>
            </article>

            {/* CTA Card */}
            <article className="about-card about-card--cta">
              <p className="about-cta-text">Cada kilómetro pedalea por ellos. Cada euro cuenta.</p>

              <a
                className="about-cta-button"
                href="https://www.dalecandela.org/"
                target="_blank"
                rel="noreferrer"
              >
                Conoce más sobre la Fundación <span className="about-cta-arrow" aria-hidden="true">→</span>
              </a>
            </article>
          </div>
        </div>
      </section>
    </main>
  );
};

export default About;
