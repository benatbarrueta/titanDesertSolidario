import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ChallengeDetail.css';
import { apiClient } from '../apiClient';

const ChallengeDetail = () => {
  const { challengeId } = useParams();
  const [challenge, setChallenge] = useState(null);
  const [warriors, setWarriors] = useState([]);
  const [selectedOptionId, setSelectedOptionId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([apiClient.getChallengeById(challengeId), apiClient.getWarriors()])
      .then(([challengeData, warriorsData]) => {
        setChallenge(challengeData);
        setWarriors(warriorsData);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [challengeId]);

  const selectedOption = useMemo(() => {
    if (!challenge || !selectedOptionId) return null;
    return challenge.options.find((o) => o.id === selectedOptionId) || null;
  }, [challenge, selectedOptionId]);

  if (loading) return <p>Cargando...</p>;
  if (error) return <p>Error: {error}</p>;

  const renderPredictionFields = () => {
    if (!selectedOption) return null;

    const n = selectedOption.number_of_selections ?? 1;

    return (
      <>
        {Array.from({ length: n }, (_, i) => (
          <select key={i} required>
            <option value="">{`Selecciona corredor ${i + 1}...`}</option>
            {warriors.map((warrior) => (
              <option key={warrior.id} value={warrior.id}>
                {warrior.name}
              </option>
            ))}
          </select>
        ))}
      </>
    );
  };

  return (
    <div className="challenge-detail">
      <h1 className='challenge-detail-title'>{challenge.icon} {challenge.title}</h1>

      <p className='challenge-detail-description'>{challenge.description}</p>

      <div className="challenge-options">
        {challenge.options.map((option) => (
          <div
            key={option.id}
            className={`challenge-option-card ${selectedOptionId === option.id ? 'selected' : ''}`}
            onClick={() => setSelectedOptionId(option.id)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                setSelectedOptionId(option.id);
              }
            }}
          >
            <div className="challenge-option-header">
              <h3>{option.name}</h3>
              <span className="challenge-option-price">€{challenge.price}</span>
            </div>
            <p className="challenge-option-description">
              {option.number_of_selections === 1
                ? `Selecciona a 1 corredor`
                : `Selecciona a ${option.number_of_selections} corredores`}
            </p>
          </div>
        ))}
      </div>

      {selectedOption && (
        <form className="challenge-form">
          <h2>{selectedOption.name}</h2>

          <label>
            Tu Nombre *
            <input type="text" placeholder="¿Cómo te llamas?" required />
          </label>

          <label>
            Email (opcional)
            <input type="email" placeholder="tu@email.com" />
          </label>

          <label>
            Tu Predicción *
            {renderPredictionFields()}
          </label>

          <label>
            Importe (mínimo €{challenge.price}) *
            <input
              type="number"
              min={challenge.price}
              defaultValue={challenge.price}
              required
            />
          </label>

          <label>
            Mensaje de Ánimo (opcional)
            <textarea placeholder="Deja tu mensaje..."></textarea>
          </label>

          <button type="submit" className="challenge-submit-button">
            🧡 Participar y Apoyar
          </button>
        </form>
      )}
    </div>
  );
};

export default ChallengeDetail;
