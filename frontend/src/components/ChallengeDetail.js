import React, { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import '../styles/ChallengeDetail.css';
import { apiClient } from '../apiClient';

const ChallengeDetail = () => {
  const { challengeId } = useParams();

  const [challenge, setChallenge] = useState(null);
  const [warriors, setWarriors] = useState([]);

  const [selectedOptionId, setSelectedOptionId] = useState(null);

  const [participantName, setParticipantName] = useState('');
  const [email, setEmail] = useState('');
  const [amount, setAmount] = useState('');
  const [message, setMessage] = useState('');

  const [selections, setSelections] = useState([]); // array de warrior ids

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    setSuccessMessage(null);
    setSelectedOptionId(null);
    setSelections([]);
    setParticipantName('');
    setEmail('');
    setMessage('');
    setAmount('');

    Promise.all([apiClient.getChallengeById(challengeId), apiClient.getWarriors()])
      .then(([challengeData, warriorsData]) => {
        setChallenge(challengeData);
        setWarriors(warriorsData);
        // amount default = precio mínimo
        setAmount(String(challengeData?.price ?? ''));
        setLoading(false);
      })
      .catch(err => {
        setError(err.message || 'Error cargando el reto');
        setLoading(false);
      });
  }, [challengeId]);

  const selectedOption = useMemo(() => {
    if (!challenge || selectedOptionId == null) return null;
    // option.id normalmente es number desde backend
    return challenge.options.find((o) => Number(o.id) === Number(selectedOptionId)) || null;
  }, [challenge, selectedOptionId]);

  // Cuando cambia la opción, ajusta el tamaño de selections
  useEffect(() => {
    if (!selectedOption) return;
    const n = selectedOption.number_of_selections ?? 1;
    setSelections(Array.from({ length: n }, (_, i) => selections[i] ?? ''));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selectedOptionId]);

  const handleChangeSelection = (index, warriorId) => {
    setSelections(prev => {
      const next = [...prev];
      next[index] = warriorId;
      return next;
    });
  };

  const canSubmit = (() => {
    if (!selectedOption || !challenge) return false;
    const min = Number(challenge.price ?? 0);
    const amt = Number(amount);
    if (!participantName.trim()) return false;
    if (!Number.isFinite(amt) || amt < min) return false;
    if (selections.length !== (selectedOption.number_of_selections ?? 1)) return false;
    if (selections.some(v => !v)) return false;
    // evitar duplicados
    const uniq = new Set(selections);
    if (uniq.size !== selections.length) return false;
    return true;
  })();

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!selectedOption || !challenge) return;

    setSubmitting(true);
    setError(null);
    setSuccessMessage(null);

    try {
      await apiClient.createParticipation({
        challenge_id: challenge.id,
        option_id: Number(selectedOption.id),
        participant_name: participantName.trim(),
        email: email.trim() ? email.trim() : null,
        prediction: { 
          selections
        },
        amount: Number(amount),
        message: message.trim() ? message.trim() : null,
      });

      setSuccessMessage('¡Participación registrada con éxito!');
      // reset parcial
      setSelections(selections.map(() => ''));
      setMessage('');
      setEmail('');
      // mantener nombre e importe si quieres; aquí los mantenemos
    } catch (err) {
      setError(err.message || 'No se pudo registrar la participación');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <p>Cargando...</p>;
  if (error && !challenge) return <p>Error: {error}</p>;
  if (!challenge) return <p>Reto no encontrado</p>;

  const renderPredictionFields = () => {
    if (!selectedOption) return null;

    const n = selectedOption.number_of_selections ?? 1;

    return (
      <>
        {Array.from({ length: n }, (_, i) => (
          <select
            key={i}
            required
            value={selections[i] ?? ''}
            onChange={(e) => handleChangeSelection(i, e.target.value)}
          >
            <option value="">{`Selecciona corredor ${i + 1}...`}</option>
            {warriors.map((warrior) => {
              const alreadySelected = selections.includes(warrior.id) && selections[i] !== warrior.id;
              return (
                <option key={warrior.id} value={warrior.id} disabled={alreadySelected}>
                  {warrior.name}
                </option>
              );
            })}
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
            className={`challenge-option-card ${Number(selectedOptionId) === Number(option.id) ? 'selected' : ''}`}
            onClick={() => setSelectedOptionId(Number(option.id))}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') setSelectedOptionId(Number(option.id));
            }}
          >
            <div className="challenge-option-header">
              <h3>{option.name}</h3>
              <span className="challenge-option-price">€{challenge.price}</span>
            </div>
            <p className="challenge-option-description">
              {option.number_of_selections === 1
                ? 'Selecciona a 1 corredor'
                : `Selecciona a ${option.number_of_selections} corredores`}
            </p>
          </div>
        ))}
      </div>

      {selectedOption && (
        <form className="challenge-form" onSubmit={onSubmit}>
          <h2>{selectedOption.name}</h2>

          <label>
            Tu Nombre *
            <input
              type="text"
              placeholder="¿Cómo te llamas?"
              required
              value={participantName}
              onChange={(e) => setParticipantName(e.target.value)}
            />
          </label>

          <label>
            Email (opcional)
            <input
              type="email"
              placeholder="tu@email.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
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
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              required
            />
          </label>

          <label>
            Mensaje de Ánimo (opcional)
            <textarea
              placeholder="Deja tu mensaje..."
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </label>

          <button type="submit" className="challenge-submit-button" disabled={!canSubmit || submitting}>
            {submitting ? 'Enviando...' : '🧡 Participar y Apoyar'}
          </button>

          {successMessage && <p className="success-message">{successMessage}</p>}
          {error && <p className="error-message">{error}</p>}
        </form>
      )}
    </div>
  );
};

export default ChallengeDetail;