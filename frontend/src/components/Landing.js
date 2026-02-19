import React, { useEffect, useState } from 'react';
import { NavLink } from 'react-router-dom';
import '../styles/Landing.css';
import { apiClient } from '../apiClient';

const Landing = () => {
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [warriors, setWarriors] = useState([]);

    useEffect(() => {
        window.scrollTo(0, 0);
        Promise.all([apiClient.getStats(), apiClient.getWarriors()])
            .then(([statsData, warriorsData]) => {
                setStats(statsData);
                setWarriors(warriorsData);
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
        <div className="landing">
            <div className="landing-sector1">
                <h1 className="landing-title">{warriors.length} GUERREROS · 650KM DE DESIERTO · 1 MISIÓN</h1>

                <p className="landing-subtitle">Únete a la lucha contra la ELA</p>

                <div className="landing-obtained-money">
                    <p className="obtained-money-title">Recaudado hasta ahora</p>
                    <p className="obtained-money-amount">€{stats.total_raised}</p>
                    <p className="obtained-money-participations">{stats.total_participations} participaciones solidarias</p>
                </div>

                <div className="landing-navlinks">
                    <NavLink to="/challenges" className="landing-navlink-about">Participa Ahora 🔥 </NavLink>
                    <NavLink to="/team" className="landing-navlink-team">Ver Equipo 👥</NavLink>
                </div>
            </div>

            <div className="landing-sector2">
                <div className="landing-stat">
                    <p className="landing-stat-number">{warriors.length}</p>
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
            </div>
        </div>
    );
};

export default Landing;