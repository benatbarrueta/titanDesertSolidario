import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAdminAuth } from "./AdminAuthContext";

const AdminAuthCallback = () => {
  const navigate = useNavigate();
  const { login } = useAdminAuth();

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");

    if (token) {
      login(token);
      navigate("/admin", { replace: true });
    } else {
      navigate("/admin/login", { replace: true });
    }
  }, [login, navigate]);

  return <p>Iniciando sesión...</p>;
};

export default AdminAuthCallback;