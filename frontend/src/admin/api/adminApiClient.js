const API_BASE_URL = "/api/v1";

const adminFetch = async (endpoint, options = {}) => {
  const token = localStorage.getItem("admin_token");

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    ...options,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Error HTTP ${response.status}`);
  }

  // Para DELETE o respuestas vacías
  if (response.status === 204) {
    return null;
  }

  return response.json();
};

const adminUpload = async (endpoint, formData) => {
  const token = localStorage.getItem("admin_token");

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `Error HTTP ${response.status}`);
  }

  return response.json();
};

export const adminApiClient = {
  getMe: () => adminFetch("/admin/auth/me"),
  getDashboard: () => adminFetch("/admin/dashboard/"),

  getStages: () => adminFetch("/admin/stages/"),
  getStageById: (id) => adminFetch(`/admin/stages/${id}`),
  updateStage: (id, data) =>
    adminFetch(`/admin/stages/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  getChallenges: () => adminFetch("/admin/challenges/"),
  getChallengeById: (id) => adminFetch(`/admin/challenges/${id}`),
  updateChallenge: (id, data) =>
    adminFetch(`/admin/challenges/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  getParticipations: () => adminFetch("/admin/participations/"),

  getWarriors: () => adminFetch("/admin/warriors/"),
  getWarriorById: (id) => adminFetch(`/admin/warriors/${id}`),

  createWarrior: (data) =>
    adminFetch("/admin/warriors/", {
      method: "POST",
      body: JSON.stringify(data),
    }),

  updateWarrior: (id, data) =>
    adminFetch(`/admin/warriors/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),

  deleteWarrior: (id) =>
    adminFetch(`/admin/warriors/${id}`, {
      method: "DELETE",
    }),

  uploadWarriorPhoto: (id, file) => {
    const formData = new FormData();
    formData.append("file", file);
    return adminUpload(`/admin/warriors/${id}/photo`, formData);
  },

  getStageResults: () => adminFetch("/admin/stage-results/"),
};