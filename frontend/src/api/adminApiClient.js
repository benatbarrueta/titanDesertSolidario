const API_BASE = "/api/v1";

export const adminFetch = async (endpoint, options = {}) => {
  const token = localStorage.getItem("admin_token");

  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    ...options,
  });

  if (!res.ok) {
    throw new Error("Admin API error");
  }

  return res.json();
};