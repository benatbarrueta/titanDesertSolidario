import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ChallengeDetail.css';

const mockChallenges = [
  {
    id: 'orden-y-posicion',
    title: 'Orden y Posición',
    description: 'Predice el orden y posición de los ciclistas en la carrera.',
    price: 5,
    icon: '🏁',
    options: [
      {
        id: '1',
        name: '1º del Equipo',
        description: 'Predice quién será el primero del equipo.',
        type: 'ranking',
        numberOfSelections: 1
      },
      {
        id: '2',
        name: 'Top 3 del Equipo (sin orden)',
        description: 'Selecciona los tres primeros sin importar el orden.',
        type: 'ranking',
        numberOfSelections: 3
      }
    ]
  },
  {
    id: 'tiempos',
    title: 'Tiempos',
    description: 'Adivina los tiempos de los ciclistas en diferentes etapas.',
    price: 8,
    icon: '⏱️',
    options: [
      {
        id: '1',
        name: 'Tiempo total de [Corredor]',
        description: 'Predice el tiempo total de un corredor.',
        type: 'text'
      },
      {
        id: '2',
        name: 'Tiempo hasta primer pinchazo',
        description: 'Adivina el tiempo hasta el primer pinchazo.',
        type: 'text'
      }
    ]
  }
];

const ChallengeDetail = () => {
  const { challengeId } = useParams();
  const [challenge, setChallenge] = useState(null);
  const [selectedOptionId, setSelectedOptionId] = useState(null);

  useEffect(() => {
    const data = mockChallenges.find((c) => c.id === challengeId) || null;
    setChallenge(data);
    setSelectedOptionId(null);
  }, [challengeId]);

  const selectedOption = useMemo(() => {
    if (!challenge || !selectedOptionId) return null;
    return challenge.options.find((o) => o.id === selectedOptionId) || null;
  }, [challenge, selectedOptionId]);

  if (!challenge) return <p>Cargando...</p>;

  const renderPredictionFields = () => {
    if (!selectedOption) return null;

    if (selectedOption.type === 'ranking') {
      const n = selectedOption.numberOfSelections ?? 1;

      return (
        <>
          {Array.from({ length: n }, (_, i) => (
            <select key={i} required>
              <option value="">{`Selecciona corredor ${i + 1}...`}</option>
              {Array.from({ length: 25 }, (_, j) => (
                <option key={j} value={`Corredor ${j + 1}`}>
                  {`Corredor ${j + 1}`}
                </option>
              ))}
            </select>
          ))}
        </>
      );
    }

    return (
      <input
        type="text"
        placeholder="Introduce tu predicción..."
        required
      />
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

            <p className='challenge-option-description'>{option.description}</p>
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
