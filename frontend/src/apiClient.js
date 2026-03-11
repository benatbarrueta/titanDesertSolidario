const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "/api/v1";

const apiFetch = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  console.log("API_FETCH_URL:", url);

  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-store",
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Error HTTP ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message || "Error de red");
  }
};

export const apiClient = {
  getStats: () => apiFetch("/stats/"),
  getStages: () => apiFetch("/stages/"),
  getWarriors: () => apiFetch("/warriors/"),
  getChallenges: () => apiFetch("/challenges/"),
  getChallengeById: (id) => apiFetch(`/challenges/${id}`),
  createParticipation: (data) =>
    apiFetch("/participations/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
};