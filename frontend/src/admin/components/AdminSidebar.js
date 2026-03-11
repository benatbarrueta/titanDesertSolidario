import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAdminAuth } from "../auth/AdminAuthContext";

const AdminSidebar = () => {
  const navigate = useNavigate();
  const { logout } = useAdminAuth();

  const handleLogout = () => {
    logout();
    navigate("/admin/login", { replace: true });
  };

  const linkStyle = ({ isActive }) => ({
    display: "block",
    padding: "12px 14px",
    borderRadius: "10px",
    textDecoration: "none",
    color: isActive ? "#111" : "#fff",
    background: isActive ? "#E0B07A" : "transparent",
    marginBottom: "8px",
    fontWeight: 500,
  });

  return (
    <aside style={styles.sidebar}>
      <div>
        <h2 style={styles.title}>Titan Admin</h2>

        <nav>
          <NavLink to="/admin" end style={linkStyle}>
            Dashboard
          </NavLink>

          <NavLink to="/admin/stages" style={linkStyle}>
            Stages
          </NavLink>

          <NavLink to="/admin/challenges" style={linkStyle}>
            Challenges
          </NavLink>

          <NavLink to="/admin/participations" style={linkStyle}>
            Participations
          </NavLink>

          <NavLink to="/admin/warriors" style={linkStyle}>
            Warriors
          </NavLink>
        </nav>
      </div>

      <button onClick={handleLogout} style={styles.logoutButton}>
        Logout
      </button>
    </aside>
  );
};

const styles = {
  sidebar: {
    width: "260px",
    minHeight: "100vh",
    background: "#111",
    color: "#fff",
    padding: "24px 18px",
    boxSizing: "border-box",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    borderRight: "1px solid #222",
  },
  title: {
    margin: "0 0 24px 0",
    fontSize: "26px",
  },
  logoutButton: {
    padding: "12px 14px",
    borderRadius: "10px",
    border: "none",
    cursor: "pointer",
    background: "#E0B07A",
    color: "#111",
    fontWeight: 600,
  },
};

export default AdminSidebar;