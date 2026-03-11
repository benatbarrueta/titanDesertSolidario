import React, { useEffect, useState } from "react";
import AdminLayout from "../components/AdminLayout";
import { adminApiClient } from "../api/adminApiClient";

const AdminStages = () => {
  const [stages, setStages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedStage, setSelectedStage] = useState(null);
  const [form, setForm] = useState({
    name: "",
    distance_km: "",
    is_published: false,
    is_open_for_contributions: false,
    is_archived: false,
    sort_order: 0,
    notes: "",
  });
  const [saving, setSaving] = useState(false);

  const loadStages = () => {
    setLoading(true);
    setError("");

    adminApiClient
      .getStages()
      .then((res) => {
        setStages(Array.isArray(res) ? res : []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Error loading stages");
        setLoading(false);
      });
  };

  useEffect(() => {
    loadStages();
  }, []);

  const startEdit = (stage) => {
    setSelectedStage(stage);
    setForm({
      name: stage.name ?? "",
      distance_km: stage.distance_km ?? "",
      is_published: !!stage.is_published,
      is_open_for_contributions: !!stage.is_open_for_contributions,
      is_archived: !!stage.is_archived,
      sort_order: stage.sort_order ?? 0,
      notes: stage.notes ?? "",
    });
  };

  const cancelEdit = () => {
    setSelectedStage(null);
    setForm({
      name: "",
      distance_km: "",
      is_published: false,
      is_open_for_contributions: false,
      is_archived: false,
      sort_order: 0,
      notes: "",
    });
  };

  const onChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const saveStage = async (e) => {
    e.preventDefault();
    if (!selectedStage) return;

    setSaving(true);
    setError("");

    try {
      await adminApiClient.updateStage(selectedStage.id, {
        name: form.name,
        distance_km: Number(form.distance_km),
        is_published: form.is_published,
        is_open_for_contributions: form.is_open_for_contributions,
        is_archived: form.is_archived,
        sort_order: Number(form.sort_order),
        notes: form.notes || null,
      });

      await loadStages();
      cancelEdit();
    } catch (err) {
      setError(err.message || "Error saving stage");
    } finally {
      setSaving(false);
    }
  };

  return (
    <AdminLayout>
      {loading && <p>Cargando stages...</p>}
      {error && <p style={{ color: "#ff8b8b" }}>Error: {error}</p>}

      {!loading && !error && (
        <div style={styles.wrapper}>
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>ID</th>
                  <th style={styles.th}>#</th>
                  <th style={styles.th}>Name</th>
                  <th style={styles.th}>Distance</th>
                  <th style={styles.th}>Published</th>
                  <th style={styles.th}>Open</th>
                  <th style={styles.th}>Archived</th>
                  <th style={styles.th}>Sort</th>
                  <th style={styles.th}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {stages.map((stage) => (
                  <tr key={stage.id}>
                    <td style={styles.td}>{stage.id}</td>
                    <td style={styles.td}>{stage.stage_number}</td>
                    <td style={styles.td}>{stage.name}</td>
                    <td style={styles.td}>{stage.distance_km} km</td>
                    <td style={styles.td}>{stage.is_published ? "Sí" : "No"}</td>
                    <td style={styles.td}>
                      {stage.is_open_for_contributions ? "Sí" : "No"}
                    </td>
                    <td style={styles.td}>{stage.is_archived ? "Sí" : "No"}</td>
                    <td style={styles.td}>{stage.sort_order}</td>
                    <td style={styles.td}>
                      <button
                        style={styles.editButton}
                        onClick={() => startEdit(stage)}
                      >
                        Editar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selectedStage && (
            <div style={styles.editor}>
              <h2 style={styles.editorTitle}>Editar Stage: {selectedStage.id}</h2>

              <form onSubmit={saveStage} style={styles.form}>
                <label style={styles.label}>
                  Name
                  <input
                    style={styles.input}
                    value={form.name}
                    onChange={(e) => onChange("name", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Distance (km)
                  <input
                    style={styles.input}
                    type="number"
                    step="0.1"
                    value={form.distance_km}
                    onChange={(e) => onChange("distance_km", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Sort order
                  <input
                    style={styles.input}
                    type="number"
                    value={form.sort_order}
                    onChange={(e) => onChange("sort_order", e.target.value)}
                  />
                </label>

                <label style={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={form.is_published}
                    onChange={(e) => onChange("is_published", e.target.checked)}
                  />
                  Published
                </label>

                <label style={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={form.is_open_for_contributions}
                    onChange={(e) =>
                      onChange("is_open_for_contributions", e.target.checked)
                    }
                  />
                  Open for contributions
                </label>

                <label style={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={form.is_archived}
                    onChange={(e) => onChange("is_archived", e.target.checked)}
                  />
                  Archived
                </label>

                <label style={styles.label}>
                  Notes
                  <textarea
                    style={styles.textarea}
                    value={form.notes}
                    onChange={(e) => onChange("notes", e.target.value)}
                  />
                </label>

                <div style={styles.actions}>
                  <button type="submit" style={styles.saveButton} disabled={saving}>
                    {saving ? "Guardando..." : "Guardar"}
                  </button>
                  <button
                    type="button"
                    style={styles.cancelButton}
                    onClick={cancelEdit}
                    disabled={saving}
                  >
                    Cancelar
                  </button>
                </div>
              </form>
            </div>
          )}
        </div>
      )}
    </AdminLayout>
  );
};

const styles = {
  wrapper: {
    display: "grid",
    gridTemplateColumns: "1.5fr 1fr",
    gap: "20px",
  },
  tableWrapper: {
    background: "#151515",
    border: "1px solid #222",
    borderRadius: "16px",
    overflow: "hidden",
  },
  table: {
    width: "100%",
    borderCollapse: "collapse",
  },
  th: {
    textAlign: "left",
    padding: "14px",
    background: "#1c1c1c",
    color: "#E0B07A",
    borderBottom: "1px solid #222",
  },
  td: {
    padding: "14px",
    borderBottom: "1px solid #222",
    color: "#fff",
    verticalAlign: "top",
  },
  editButton: {
    padding: "8px 12px",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    background: "#E0B07A",
    color: "#111",
    fontWeight: 600,
  },
  editor: {
    background: "#151515",
    border: "1px solid #222",
    borderRadius: "16px",
    padding: "20px",
  },
  editorTitle: {
    marginTop: 0,
    marginBottom: "16px",
  },
  form: {
    display: "grid",
    gap: "14px",
  },
  label: {
    display: "grid",
    gap: "8px",
  },
  input: {
    padding: "10px 12px",
    borderRadius: "10px",
    border: "1px solid #333",
    background: "#0f0f0f",
    color: "#fff",
  },
  textarea: {
    minHeight: "100px",
    padding: "10px 12px",
    borderRadius: "10px",
    border: "1px solid #333",
    background: "#0f0f0f",
    color: "#fff",
    resize: "vertical",
  },
  checkboxLabel: {
    display: "flex",
    gap: "10px",
    alignItems: "center",
  },
  actions: {
    display: "flex",
    gap: "12px",
  },
  saveButton: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    background: "#E0B07A",
    color: "#111",
    fontWeight: 700,
  },
  cancelButton: {
    padding: "10px 16px",
    border: "1px solid #333",
    borderRadius: "10px",
    cursor: "pointer",
    background: "transparent",
    color: "#fff",
  },
};

export default AdminStages;