import React, { useEffect, useState } from "react";
import AdminLayout from "../components/AdminLayout";
import { adminApiClient } from "../api/adminApiClient";

const AdminChallenges = () => {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [form, setForm] = useState({
    title: "",
    description: "",
    price: "",
    icon: "",
    is_active: false,
    is_published: false,
    is_archived: false,
    sort_order: 0,
  });
  const [saving, setSaving] = useState(false);

  const loadChallenges = () => {
    setLoading(true);
    setError("");

    adminApiClient
      .getChallenges()
      .then((res) => {
        setChallenges(Array.isArray(res) ? res : []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Error loading challenges");
        setLoading(false);
      });
  };

  useEffect(() => {
    loadChallenges();
  }, []);

  const startEdit = (challenge) => {
    setSelectedChallenge(challenge);
    setForm({
      title: challenge.title ?? "",
      description: challenge.description ?? "",
      price: challenge.price ?? "",
      icon: challenge.icon ?? "",
      is_active: !!challenge.is_active,
      is_published: !!challenge.is_published,
      is_archived: !!challenge.is_archived,
      sort_order: challenge.sort_order ?? 0,
    });
  };

  const cancelEdit = () => {
    setSelectedChallenge(null);
    setForm({
      title: "",
      description: "",
      price: "",
      icon: "",
      is_active: false,
      is_published: false,
      is_archived: false,
      sort_order: 0,
    });
  };

  const onChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const saveChallenge = async (e) => {
    e.preventDefault();
    if (!selectedChallenge) return;

    setSaving(true);
    setError("");

    try {
      await adminApiClient.updateChallenge(selectedChallenge.id, {
        title: form.title,
        description: form.description,
        price: Number(form.price),
        icon: form.icon,
        is_active: form.is_active,
        is_published: form.is_published,
        is_archived: form.is_archived,
        sort_order: Number(form.sort_order),
      });

      await loadChallenges();
      cancelEdit();
    } catch (err) {
      setError(err.message || "Error saving challenge");
    } finally {
      setSaving(false);
    }
  };

  return (
    <AdminLayout>
      {loading && <p>Cargando challenges...</p>}
      {error && <p style={{ color: "#ff8b8b" }}>Error: {error}</p>}

      {!loading && !error && (
        <div style={styles.wrapper}>
          <div style={styles.tableWrapper}>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>ID</th>
                  <th style={styles.th}>Title</th>
                  <th style={styles.th}>Price</th>
                  <th style={styles.th}>Published</th>
                  <th style={styles.th}>Active</th>
                  <th style={styles.th}>Options</th>
                  <th style={styles.th}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {challenges.map((item) => (
                  <tr key={item.id}>
                    <td style={styles.td}>{item.id}</td>
                    <td style={styles.td}>{item.title}</td>
                    <td style={styles.td}>{item.price} €</td>
                    <td style={styles.td}>{item.is_published ? "Sí" : "No"}</td>
                    <td style={styles.td}>{item.is_active ? "Sí" : "No"}</td>
                    <td style={styles.td}>{item.options_count}</td>
                    <td style={styles.td}>
                      <button
                        style={styles.editButton}
                        onClick={() => startEdit(item)}
                      >
                        Editar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {selectedChallenge && (
            <div style={styles.editor}>
              <h2 style={styles.editorTitle}>
                Editar Challenge: {selectedChallenge.id}
              </h2>

              <form onSubmit={saveChallenge} style={styles.form}>
                <label style={styles.label}>
                  Title
                  <input
                    style={styles.input}
                    value={form.title}
                    onChange={(e) => onChange("title", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Description
                  <textarea
                    style={styles.textarea}
                    value={form.description}
                    onChange={(e) => onChange("description", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Price
                  <input
                    style={styles.input}
                    type="number"
                    step="0.01"
                    value={form.price}
                    onChange={(e) => onChange("price", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Icon
                  <input
                    style={styles.input}
                    value={form.icon}
                    onChange={(e) => onChange("icon", e.target.value)}
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
                    checked={form.is_active}
                    onChange={(e) => onChange("is_active", e.target.checked)}
                  />
                  Active
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
                    checked={form.is_archived}
                    onChange={(e) => onChange("is_archived", e.target.checked)}
                  />
                  Archived
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

export default AdminChallenges;