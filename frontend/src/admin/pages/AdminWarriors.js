import React, { useEffect, useMemo, useState } from "react";
import AdminLayout from "../components/AdminLayout";
import { adminApiClient } from "../api/adminApiClient";

const BACKEND_BASE_URL =
  process.env.REACT_APP_BACKEND_BASE_URL || "http://localhost:8000";

const buildPhotoUrl = (photoUrl) => {
  if (!photoUrl) return null;
  if (photoUrl.startsWith("http://") || photoUrl.startsWith("https://")) {
    return photoUrl;
  }
  return `${BACKEND_BASE_URL}${photoUrl}`;
};

const emptyForm = {
  id: "",
  name: "",
  dorsal: "",
  raised_cache: "",
  photo_url: "",
};

const AdminWarriors = () => {
  const [warriors, setWarriors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const [selectedWarrior, setSelectedWarrior] = useState(null);
  const [isCreating, setIsCreating] = useState(false);
  const [form, setForm] = useState(emptyForm);

  const [saving, setSaving] = useState(false);
  const [uploadingPhoto, setUploadingPhoto] = useState(false);
  const [deleting, setDeleting] = useState(false);

  const [selectedFile, setSelectedFile] = useState(null);
  const [localPreview, setLocalPreview] = useState("");

  const sortedWarriors = useMemo(() => {
    return [...warriors].sort((a, b) => (a.dorsal ?? 0) - (b.dorsal ?? 0));
  }, [warriors]);

  const clearMessages = () => {
    setError("");
    setSuccessMessage("");
  };

  const loadWarriors = () => {
    setLoading(true);
    clearMessages();

    adminApiClient
      .getWarriors()
      .then((res) => {
        setWarriors(Array.isArray(res) ? res : []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Error loading warriors");
        setLoading(false);
      });
  };

  useEffect(() => {
    loadWarriors();
  }, []);

  useEffect(() => {
    return () => {
      if (localPreview) {
        URL.revokeObjectURL(localPreview);
      }
    };
  }, [localPreview]);

  const resetPreview = () => {
    if (localPreview) {
      URL.revokeObjectURL(localPreview);
      setLocalPreview("");
    }
    setSelectedFile(null);
  };

  const startCreate = () => {
    clearMessages();
    setSelectedWarrior(null);
    setIsCreating(true);
    setForm(emptyForm);
    resetPreview();
  };

  const startEdit = (warrior) => {
    clearMessages();
    setIsCreating(false);
    setSelectedWarrior(warrior);
    setForm({
      id: warrior.id ?? "",
      name: warrior.name ?? "",
      dorsal: warrior.dorsal ?? "",
      raised_cache: warrior.raised_cache ?? 0,
      photo_url: warrior.photo_url ?? "",
    });
    resetPreview();
  };

  const cancelEdit = () => {
    setSelectedWarrior(null);
    setIsCreating(false);
    setForm(emptyForm);
    resetPreview();
    clearMessages();
  };

  const onChange = (field, value) => {
    setForm((prev) => ({ ...prev, [field]: value }));
  };

  const onFileChange = (e) => {
    const file = e.target.files?.[0] || null;
    setSelectedFile(file);

    if (localPreview) {
      URL.revokeObjectURL(localPreview);
      setLocalPreview("");
    }

    if (file) {
      const objectUrl = URL.createObjectURL(file);
      setLocalPreview(objectUrl);
    }
  };

  const saveWarrior = async (e) => {
    e.preventDefault();
    clearMessages();
    setSaving(true);

    try {
      if (isCreating) {
        const created = await adminApiClient.createWarrior({
          id: form.id.trim(),
          name: form.name.trim(),
          dorsal: Number(form.dorsal),
          raised_cache: Number(form.raised_cache || 0),
          photo_url: null,
        });

        setSelectedWarrior(created);
        setIsCreating(false);
        setForm({
          id: created.id ?? "",
          name: created.name ?? "",
          dorsal: created.dorsal ?? "",
          raised_cache: created.raised_cache ?? 0,
          photo_url: created.photo_url ?? "",
        });

        setSuccessMessage("Warrior creado correctamente.");
      } else if (selectedWarrior) {
        const updated = await adminApiClient.updateWarrior(selectedWarrior.id, {
          name: form.name.trim(),
          dorsal: Number(form.dorsal),
          raised_cache: Number(form.raised_cache || 0),
        });

        setSelectedWarrior(updated);
        setForm((prev) => ({
          ...prev,
          name: updated.name ?? "",
          dorsal: updated.dorsal ?? "",
          raised_cache: updated.raised_cache ?? 0,
          photo_url: updated.photo_url ?? "",
        }));

        setSuccessMessage("Warrior actualizado correctamente.");
      }

      await loadWarriors();
    } catch (err) {
      setError(err.message || "Error saving warrior");
    } finally {
      setSaving(false);
    }
  };

  const uploadPhoto = async () => {
    if (!selectedWarrior || !selectedFile) return;

    clearMessages();
    setUploadingPhoto(true);

    try {
      const updated = await adminApiClient.uploadWarriorPhoto(
        selectedWarrior.id,
        selectedFile
      );

      setSelectedWarrior(updated);
      setForm((prev) => ({
        ...prev,
        photo_url: updated.photo_url ?? "",
      }));

      resetPreview();
      setSuccessMessage("Foto subida correctamente.");

      await loadWarriors();
    } catch (err) {
      setError(err.message || "Error uploading warrior photo");
    } finally {
      setUploadingPhoto(false);
    }
  };

  const deleteWarrior = async () => {
    if (!selectedWarrior) return;

    const confirmed = window.confirm(
      `¿Seguro que quieres eliminar a ${selectedWarrior.name}?`
    );

    if (!confirmed) return;

    clearMessages();
    setDeleting(true);

    try {
      await adminApiClient.deleteWarrior(selectedWarrior.id);
      setSuccessMessage("Warrior eliminado correctamente.");
      cancelEdit();
      await loadWarriors();
    } catch (err) {
      setError(err.message || "Error deleting warrior");
    } finally {
      setDeleting(false);
    }
  };

  const previewSrc = localPreview || buildPhotoUrl(form.photo_url) || null;
  const showEditor = isCreating || !!selectedWarrior;

  return (
    <AdminLayout>
      {loading && <p>Cargando warriors...</p>}
      {error && <p style={{ color: "#ff8b8b" }}>Error: {error}</p>}
      {successMessage && <p style={{ color: "#8bffb0" }}>{successMessage}</p>}

      {!loading && (
        <div style={styles.wrapper}>
          <div style={styles.tableWrapper}>
            <div style={styles.tableHeader}>
              <h2 style={styles.tableTitle}>Lista de corredores</h2>
              <button style={styles.createButton} onClick={startCreate}>
                + Nuevo warrior
              </button>
            </div>

            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>Photo</th>
                  <th style={styles.th}>ID</th>
                  <th style={styles.th}>Dorsal</th>
                  <th style={styles.th}>Name</th>
                  <th style={styles.th}>Raised</th>
                  <th style={styles.th}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {sortedWarriors.map((warrior) => (
                  <tr key={warrior.id}>
                    <td style={styles.td}>
                      {warrior.photo_url ? (
                        <img
                          src={buildPhotoUrl(warrior.photo_url)}
                          alt={warrior.name}
                          style={styles.avatar}
                        />
                      ) : (
                        <div style={styles.avatarPlaceholder}>No photo</div>
                      )}
                    </td>
                    <td style={styles.td}>{warrior.id}</td>
                    <td style={styles.td}>{warrior.dorsal}</td>
                    <td style={styles.td}>{warrior.name}</td>
                    <td style={styles.td}>{warrior.raised_cache ?? 0} €</td>
                    <td style={styles.td}>
                      <button
                        style={styles.editButton}
                        onClick={() => startEdit(warrior)}
                      >
                        Editar
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {showEditor && (
            <div style={styles.editor}>
              <h2 style={styles.editorTitle}>
                {isCreating
                  ? "Crear nuevo warrior"
                  : `Editar warrior: ${selectedWarrior.id}`}
              </h2>

              <form onSubmit={saveWarrior} style={styles.form}>
                {isCreating && (
                  <label style={styles.label}>
                    ID
                    <input
                      style={styles.input}
                      value={form.id}
                      onChange={(e) => onChange("id", e.target.value)}
                      placeholder="beltran"
                    />
                  </label>
                )}

                <label style={styles.label}>
                  Name
                  <input
                    style={styles.input}
                    value={form.name}
                    onChange={(e) => onChange("name", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Dorsal
                  <input
                    style={styles.input}
                    type="number"
                    value={form.dorsal}
                    onChange={(e) => onChange("dorsal", e.target.value)}
                  />
                </label>

                <label style={styles.label}>
                  Raised cache
                  <input
                    style={styles.input}
                    type="number"
                    step="0.01"
                    value={form.raised_cache}
                    onChange={(e) => onChange("raised_cache", e.target.value)}
                  />
                </label>

                <div style={styles.actions}>
                  <button type="submit" style={styles.saveButton} disabled={saving}>
                    {saving
                      ? "Guardando..."
                      : isCreating
                      ? "Crear warrior"
                      : "Guardar cambios"}
                  </button>

                  {!isCreating && (
                    <button
                      type="button"
                      style={styles.deleteButton}
                      onClick={deleteWarrior}
                      disabled={deleting || saving || uploadingPhoto}
                    >
                      {deleting ? "Eliminando..." : "Eliminar"}
                    </button>
                  )}

                  <button
                    type="button"
                    style={styles.cancelButton}
                    onClick={cancelEdit}
                    disabled={saving || uploadingPhoto || deleting}
                  >
                    Cancelar
                  </button>
                </div>
              </form>

              {!isCreating && (
                <>
                  <hr style={styles.separator} />

                  <div style={styles.photoSection}>
                    <h3 style={styles.photoTitle}>Warrior photo</h3>

                    <div style={styles.photoPreviewBox}>
                      {previewSrc ? (
                        <img
                          src={previewSrc}
                          alt="Preview"
                          style={styles.previewImage}
                        />
                      ) : (
                        <div style={styles.noPreview}>No photo uploaded</div>
                      )}
                    </div>

                    <label style={styles.fileLabel}>
                      Select image
                      <input
                        type="file"
                        accept="image/png,image/jpeg,image/webp"
                        onChange={onFileChange}
                        style={styles.fileInput}
                      />
                    </label>

                    {selectedFile && (
                      <p style={styles.fileName}>Selected: {selectedFile.name}</p>
                    )}

                    <button
                      type="button"
                      style={styles.uploadButton}
                      onClick={uploadPhoto}
                      disabled={!selectedFile || uploadingPhoto}
                    >
                      {uploadingPhoto ? "Subiendo..." : "Subir foto"}
                    </button>
                  </div>
                </>
              )}
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
  tableHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "16px",
    background: "#1c1c1c",
    borderBottom: "1px solid #222",
  },
  tableTitle: {
    margin: 0,
    color: "#fff",
    fontSize: "20px",
  },
  createButton: {
    padding: "10px 14px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    background: "#E0B07A",
    color: "#111",
    fontWeight: 700,
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
    verticalAlign: "middle",
  },
  avatar: {
    width: "56px",
    height: "56px",
    borderRadius: "12px",
    objectFit: "cover",
    display: "block",
  },
  avatarPlaceholder: {
    width: "56px",
    height: "56px",
    borderRadius: "12px",
    background: "#222",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "11px",
    color: "#aaa",
    textAlign: "center",
    padding: "4px",
    boxSizing: "border-box",
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
  actions: {
    display: "flex",
    gap: "12px",
    marginTop: "4px",
    flexWrap: "wrap",
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
  deleteButton: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    background: "#c0392b",
    color: "#fff",
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
  separator: {
    borderColor: "#222",
    margin: "24px 0",
  },
  photoSection: {
    display: "grid",
    gap: "14px",
  },
  photoTitle: {
    margin: 0,
  },
  photoPreviewBox: {
    width: "100%",
    minHeight: "220px",
    background: "#0f0f0f",
    border: "1px solid #333",
    borderRadius: "14px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    overflow: "hidden",
  },
  previewImage: {
    width: "100%",
    maxHeight: "320px",
    objectFit: "cover",
    display: "block",
  },
  noPreview: {
    color: "#888",
  },
  fileLabel: {
    display: "grid",
    gap: "8px",
  },
  fileInput: {
    color: "#fff",
  },
  fileName: {
    margin: 0,
    color: "#bbb",
    fontSize: "14px",
  },
  uploadButton: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    background: "#E0B07A",
    color: "#111",
    fontWeight: 700,
  },
};

export default AdminWarriors;