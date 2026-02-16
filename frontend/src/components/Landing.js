import React from 'react';
import { NavLink } from 'react-router-dom';

import '../styles/Landing.css';

const Landing = () => {
    return (
        <div className="landing">
            <div className="landing-sector1">
                <h1 className="landing-title">25 GUERREROS · 650KM DE DESIERTO · 1 MISIÓN</h1>
            
                <p className="landing-subtitle">Únete a la lucha contra la ELA</p>

                <div className="landing-obtained-money">
                    <p className="obtained-money-title">Recaudado hasta ahora</p>
                    <p className="obtained-money-amount">€0</p>
                    <p className="obtained-money-participations">0 participaciones solidarias</p>
                </div>

                <div className="landing-navlinks">
                    <NavLink to="/challenges" className="landing-navlink-about">Participa Ahora 🔥 </NavLink>
                    <NavLink to="/team" className="landing-navlink-team">Ver Equipo 👥</NavLink>
                </div>
            </div>

            <div className="landing-sector2">
                <div className="landing-stat">
                    <p className="landing-stat-number">25</p>
                    <p className="landing-stat-label">Ciclistas</p>
                </div>
                <div className="landing-stat">
                    <p className="landing-stat-number">650KM</p>
                    <p className="landing-stat-label">De Desierto</p>
                </div>
                <div className="landing-stat">
                    <p className="landing-stat-number">6</p>
                    <p className="landing-stat-label">Etapas</p>
                </div>
                <div className="landing-stat">
                    <p className="landing-stat-number">100%</p>
                    <p className="landing-stat-label">vs ELA</p>
                </div>
            </div>

            <div className="landing-sector3">
                <h2 className="landing-sector3-title">PARTICIPA EN LOS RETOS SOLIDARIOS</h2>
                <p className="landing-sector3-description">
                    Elige a tu ciclista favorito, haz tu predicción y apoya la investigación contra la ELA.
                    Cada participación cuenta.
                </p>
                <div className="landing-sector3-button">
                    <NavLink to="/challenges" className="landing-sector3-link">Ver Todos los Retos ➞</NavLink>
                </div>
            </div>
        </div>
    );
};

export default Landing;