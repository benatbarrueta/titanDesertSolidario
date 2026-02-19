const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000/api/v1";

const apiFetch = async (endpoint, options = {}) => {
    const url = `${API_BASE_URL}${endpoint}`;
    try {
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
            },
            ...options,
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Error desconocido");
        }

        return await response.json();
    } catch (error) {
        throw new Error(error.message || "Error de red");
    }
};

export const apiClient = {
    getStats: () => apiFetch("/stats"),
    getWarriors: () => apiFetch("/warriors"),
    getChallenges: () => apiFetch("/challenges/"),
    getChallengeById: (id) => apiFetch(`/challenges/${id}`),
    createParticipation: (data) => apiFetch(`/participations`, {
        method: "POST",
        body: JSON.stringify(data),
    }),
};