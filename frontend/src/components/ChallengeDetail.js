import React, { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import "../styles/ChallengeDetail.css";
import { apiClient } from "../apiClient";

const ChallengeDetail = () => {
  const { challengeId } = useParams();

  const [challenge, setChallenge] = useState(null);
  const [warriors, setWarriors] = useState([]);
  const [stages, setStages] = useState([]);

  const [selectedOptionId, setSelectedOptionId] = useState(null);

  // Campos comunes
  const [participantName, setParticipantName] = useState("");
  const [email, setEmail] = useState(""); // obligatorio
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");

  // subject dinámico
  const [subjectWarriorId, setSubjectWarriorId] = useState("");
  const [subjectStageId, setSubjectStageId] = useState("");

  // answer dinámico
  const [selections, setSelections] = useState([]); // warrior_pick
  const [value, setValue] = useState(""); // number/time/text/choice/boolean
  const [answerStageId, setAnswerStageId] = useState(""); // stage_choice / boolean_stage(_optional)

  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Load: challenge + warriors + stages
  useEffect(() => {
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    // reset UI
    setSelectedOptionId(null);
    setParticipantName("");
    setEmail("");
    setMessage("");
    setAmount("");

    setSubjectWarriorId("");
    setSubjectStageId("");
    setSelections([]);
    setValue("");
    setAnswerStageId("");

    Promise.all([
      apiClient.getChallengeById(challengeId),
      apiClient.getWarriors(),
      apiClient.getStages(),
    ])
      .then(([challengeData, warriorsData, stagesData]) => {
        setChallenge(challengeData);
        setWarriors(warriorsData);
        setStages(stagesData);
        setAmount(String(challengeData?.price ?? ""));
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Error cargando el reto");
        setLoading(false);
      });
  }, [challengeId]);

  const selectedOption = useMemo(() => {
    if (!challenge || selectedOptionId == null) return null;
    return (
      challenge.options.find((o) => Number(o.id) === Number(selectedOptionId)) ||
      null
    );
  }, [challenge, selectedOptionId]);

  // init dynamic form when option changes
  useEffect(() => {
    if (!selectedOption) return;

    setError(null);
    setSuccessMessage(null);

    // reset fields except common
    setSubjectWarriorId("");
    setSubjectStageId("");
    setValue("");
    setAnswerStageId("");

    if (selectedOption.answer_type === "warrior_pick") {
      const n = selectedOption.number_of_selections ?? 1;
      setSelections(Array.from({ length: n }, () => ""));
    } else {
      setSelections([]);
    }

    // fixed stage (answer)
    const fixed = selectedOption?.config?.fixed_stage_id;
    if (fixed) setAnswerStageId(fixed);
  }, [selectedOptionId]); // eslint-disable-line react-hooks/exhaustive-deps

  // helpers
  const isNonEmpty = (s) => String(s ?? "").trim().length > 0;
  const parseNumber = (s) => {
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  };

  const requiresSubjectWarrior = (opt) =>
    opt?.subject_type === "warrior" || opt?.subject_type === "warrior_stage";

  const requiresSubjectStage = (opt) =>
    opt?.subject_type === "stage" || opt?.subject_type === "warrior_stage";

  const minAmount = Number(challenge?.price ?? 0);

  const buildPrediction = () => {
    const opt = selectedOption;
    if (!opt) return null;

    const prediction = {};

    // SUBJECT
    if (requiresSubjectWarrior(opt)) prediction.warrior_id = subjectWarriorId;
    if (requiresSubjectStage(opt)) prediction.stage_id = subjectStageId;

    // ANSWER
    switch (opt.answer_type) {
      case "warrior_pick":
        prediction.selections = selections;
        break;

      case "stage_choice":
        // backend: answer_stage_id o fallback stage_id
        prediction.answer_stage_id = answerStageId;
        break;

      case "choice":
      case "text":
        prediction.value = String(value);
        break;

      case "number": {
        prediction.value = parseNumber(value);
        break;
      }

      case "time": {
        prediction.value = parseNumber(value); // seconds numeric
        break;
      }

      case "boolean":
        prediction.value = value === true || value === "true";
        break;

      case "boolean_stage":
      case "boolean_stage_optional": {
        const v = value === true || value === "true";
        prediction.value = v;
        if (answerStageId) prediction.stage_id = answerStageId; // stage attached to boolean
        break;
      }

      default:
        prediction.value = value;
        break;
    }

    // fixed answer stage enforced
    const fixed = opt?.config?.fixed_stage_id;
    if (fixed) prediction.answer_stage_id = fixed;

    return prediction;
  };

  const validate = () => {
    if (!challenge || !selectedOption) return { ok: false, msg: "Selecciona una opción" };

    if (!isNonEmpty(participantName)) return { ok: false, msg: "Tu nombre es obligatorio" };
    if (!isNonEmpty(email)) return { ok: false, msg: "El email es obligatorio" };

    const amt = parseNumber(amount);
    if (amt == null || amt < minAmount) return { ok: false, msg: `El importe mínimo es €${minAmount}` };

    const opt = selectedOption;

    // subject required
    if (requiresSubjectWarrior(opt) && !isNonEmpty(subjectWarriorId)) return { ok: false, msg: "Selecciona un corredor" };
    if (requiresSubjectStage(opt) && !isNonEmpty(subjectStageId)) return { ok: false, msg: "Selecciona una etapa" };

    // answer required
    switch (opt.answer_type) {
      case "warrior_pick": {
        const n = opt.number_of_selections ?? 1;
        if (!Array.isArray(selections) || selections.length !== n) return { ok: false, msg: "Selecciones inválidas" };
        if (selections.some((x) => !isNonEmpty(x))) return { ok: false, msg: "Completa todas las selecciones" };
        if (new Set(selections).size !== selections.length) return { ok: false, msg: "No puedes repetir corredores" };
        return { ok: true };
      }

      case "stage_choice": {
        const fixed = opt?.config?.fixed_stage_id;
        if (fixed) return { ok: true };
        if (!isNonEmpty(answerStageId)) return { ok: false, msg: "Selecciona una etapa" };
        return { ok: true };
      }

      case "choice": {
        const allowed = opt?.config?.allowed_values ?? [];
        if (!isNonEmpty(value)) return { ok: false, msg: "Selecciona una opción" };
        if (Array.isArray(allowed) && allowed.length && !allowed.includes(value)) return { ok: false, msg: "Valor no permitido" };
        return { ok: true };
      }

      case "number": {
        const n = parseNumber(value);
        if (n == null || n < 0) return { ok: false, msg: "Introduce un número válido (>=0)" };
        return { ok: true };
      }

      case "time": {
        const n = parseNumber(value);
        if (n == null || n <= 0) return { ok: false, msg: "Introduce un tiempo válido (>0) en segundos" };
        return { ok: true };
      }

      case "boolean":
        if (!(value === "true" || value === "false" || value === true || value === false)) return { ok: false, msg: "Selecciona Sí/No" };
        return { ok: true };

      case "boolean_stage":
      case "boolean_stage_optional": {
        if (!(value === "true" || value === "false" || value === true || value === false)) return { ok: false, msg: "Selecciona Sí/No" };
        const v = value === true || value === "true";
        const requiredIfTrue = !!opt?.config?.stage_required_if_true;
        if (opt.answer_type === "boolean_stage" && requiredIfTrue && v && !isNonEmpty(answerStageId)) {
          return { ok: false, msg: "Selecciona etapa" };
        }
        return { ok: true };
      }

      case "text":
        if (!isNonEmpty(value)) return { ok: false, msg: "Completa el texto" };
        return { ok: true };

      default:
        return { ok: true };
    }
  };

  const { ok: canSubmit, msg: cannotMsg } = validate();

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!selectedOption || !challenge) return;

    const v = validate();
    if (!v.ok) {
      setError(v.msg || "Formulario inválido");
      return;
    }

    setSubmitting(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const prediction = buildPrediction();

      await apiClient.createParticipation({
        challenge_id: challenge.id,
        option_id: Number(selectedOption.id),
        participant_name: participantName.trim(),
        email: email.trim(),
        prediction,
        amount: Number(amount),
        message: message?.trim() ? message.trim() : null,
      });

      setSuccessMessage("¡Participación registrada con éxito!");

      // reset only prediction fields
      setSubjectWarriorId("");
      setSubjectStageId("");
      setSelections((prev) => prev.map(() => ""));
      setValue("");
      const fixed = selectedOption?.config?.fixed_stage_id;
      setAnswerStageId(fixed || "");
      setMessage("");
    } catch (err) {
      setError(err.message || "No se pudo registrar la participación");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <p>Cargando...</p>;
  if (error && !challenge) return <p>Error: {error}</p>;
  if (!challenge) return <p>Reto no encontrado</p>;

  const renderSubjectFields = () => {
    if (!selectedOption) return null;

    return (
      <>
        {requiresSubjectWarrior(selectedOption) && (
          <label>
            Corredor *
            <select required value={subjectWarriorId} onChange={(e) => setSubjectWarriorId(e.target.value)}>
              <option value="">Selecciona corredor...</option>
              {warriors.map((w) => (
                <option key={w.id} value={w.id}>
                  {w.name}
                </option>
              ))}
            </select>
          </label>
        )}

        {requiresSubjectStage(selectedOption) && (
          <label>
            Etapa *
            <select required value={subjectStageId} onChange={(e) => setSubjectStageId(e.target.value)}>
              <option value="">Selecciona etapa...</option>
              {stages
                .slice()
                .sort((a, b) => a.stage_number - b.stage_number)
                .map((s) => (
                  <option key={s.id} value={s.id}>
                    {`Etapa ${s.stage_number} · ${s.name} (${s.distance_km}km)`}
                  </option>
                ))}
            </select>
          </label>
        )}
      </>
    );
  };

  const renderAnswerFields = () => {
    if (!selectedOption) return null;

    const opt = selectedOption;

    switch (opt.answer_type) {
      case "warrior_pick": {
        const n = opt.number_of_selections ?? 1;
        return (
          <label>
            Predicción *
            <>
              {Array.from({ length: n }, (_, i) => (
                <select
                  key={i}
                  required
                  value={selections[i] ?? ""}
                  onChange={(e) => {
                    const warriorId = e.target.value;
                    setSelections((prev) => {
                      const next = [...prev];
                      next[i] = warriorId;
                      return next;
                    });
                  }}
                >
                  <option value="">{`Selecciona corredor ${i + 1}...`}</option>
                  {warriors.map((w) => {
                    const alreadySelected = selections.includes(w.id) && selections[i] !== w.id;
                    return (
                      <option key={w.id} value={w.id} disabled={alreadySelected}>
                        {w.name}
                      </option>
                    );
                  })}
                </select>
              ))}
            </>
          </label>
        );
      }

      case "stage_choice": {
        const fixed = opt?.config?.fixed_stage_id;
        return (
          <label>
            Predicción *
            {fixed ? (
              <input value={`Etapa fija: ${fixed}`} disabled />
            ) : (
              <select required value={answerStageId} onChange={(e) => setAnswerStageId(e.target.value)}>
                <option value="">Selecciona etapa...</option>
                {stages
                  .slice()
                  .sort((a, b) => a.stage_number - b.stage_number)
                  .map((s) => (
                    <option key={s.id} value={s.id}>
                      {`Etapa ${s.stage_number} · ${s.name}`}
                    </option>
                  ))}
              </select>
            )}
          </label>
        );
      }

      case "choice": {
        const allowed = opt?.config?.allowed_values ?? [];
        return (
          <label>
            Predicción *
            <select required value={value} onChange={(e) => setValue(e.target.value)}>
              <option value="">Selecciona...</option>
              {allowed.map((v) => (
                <option key={v} value={v}>
                  {v}
                </option>
              ))}
            </select>
          </label>
        );
      }

      case "number":
        return (
          <label>
            Predicción *
            <input type="number" value={value} onChange={(e) => setValue(e.target.value)} required />
          </label>
        );

      case "time":
        return (
          <label>
            Predicción (segundos) *
            <input type="number" value={value} onChange={(e) => setValue(e.target.value)} required />
          </label>
        );

      case "boolean":
        return (
          <label>
            Predicción *
            <select required value={String(value)} onChange={(e) => setValue(e.target.value)}>
              <option value="">Selecciona...</option>
              <option value="true">Sí</option>
              <option value="false">No</option>
            </select>
          </label>
        );

      case "boolean_stage":
      case "boolean_stage_optional": {
        const requiredIfTrue = !!opt?.config?.stage_required_if_true;
        const v = value === true || value === "true";
        return (
          <>
            <label>
              Predicción *
              <select required value={String(value)} onChange={(e) => setValue(e.target.value)}>
                <option value="">Selecciona...</option>
                <option value="true">Sí</option>
                <option value="false">No</option>
              </select>
            </label>

            {(opt.answer_type === "boolean_stage_optional" || (v && requiredIfTrue)) && (
              <label>
                Etapa {v && requiredIfTrue ? "*" : "(opcional)"}
                <select
                  value={answerStageId}
                  onChange={(e) => setAnswerStageId(e.target.value)}
                  required={v && requiredIfTrue}
                >
                  <option value="">Selecciona etapa...</option>
                  {stages
                    .slice()
                    .sort((a, b) => a.stage_number - b.stage_number)
                    .map((s) => (
                      <option key={s.id} value={s.id}>
                        {`Etapa ${s.stage_number} · ${s.name}`}
                      </option>
                    ))}
                </select>
              </label>
            )}
          </>
        );
      }

      case "text":
        return (
          <label>
            Predicción *
            <input type="text" value={value} onChange={(e) => setValue(e.target.value)} required />
          </label>
        );

      default:
        return (
          <label>
            Predicción *
            <input value={value} onChange={(e) => setValue(e.target.value)} required />
          </label>
        );
    }
  };

  return (
    <div className="challenge-detail">
      <h1 className="challenge-detail-title">
        {challenge.icon} {challenge.title}
      </h1>

      <p className="challenge-detail-description">{challenge.description}</p>

      <div className="challenge-options">
        {challenge.options.map((option) => (
          <div
            key={option.id}
            className={`challenge-option-card ${Number(selectedOptionId) === Number(option.id) ? "selected" : ""}`}
            onClick={() => setSelectedOptionId(Number(option.id))}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") setSelectedOptionId(Number(option.id));
            }}
          >
            <div className="challenge-option-header">
              <h3>{option.name}</h3>
              <span className="challenge-option-price">€{challenge.price}</span>
            </div>

            <p className="challenge-option-description">
              {option.answer_type === "warrior_pick"
                ? option.number_of_selections === 1
                  ? "Selecciona a 1 corredor"
                  : `Selecciona a ${option.number_of_selections} corredores`
                : `${option.subject_type} · ${option.answer_type}`}
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
            Email *
            <input
              type="email"
              placeholder="tu@email.com"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>

          {renderSubjectFields()}
          {renderAnswerFields()}

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
            <textarea placeholder="Deja tu mensaje..." value={message} onChange={(e) => setMessage(e.target.value)} />
          </label>

          <button type="submit" className="challenge-submit-button" disabled={!canSubmit || submitting}>
            {submitting ? "Enviando..." : "🧡 Participar y Apoyar"}
          </button>

          {!canSubmit && cannotMsg && <p className="error-message">{cannotMsg}</p>}
          {successMessage && <p className="success-message">{successMessage}</p>}
          {error && <p className="error-message">{error}</p>}
        </form>
      )}
    </div>
  );
};

export default ChallengeDetail;