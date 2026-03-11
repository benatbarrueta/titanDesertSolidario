import React from "react";
import AdminSidebar from "./AdminSidebar";

const AdminLayout = ({ title, children }) => {
  return (
    <div style={styles.wrapper}>
      <AdminSidebar />

      <main style={styles.main}>
        {title && (
          <header style={styles.header}>
            <h1 style={styles.pageTitle}>{title}</h1>
          </header>
        )}

        <section>{children}</section>
      </main>
    </div>
  );
};

const styles = {
  wrapper: {
    display: "flex",
    minHeight: "100vh",
    background: "#0B0B0B",
    color: "#fff",
  },
  main: {
    flex: 1,
    padding: "24px",
    boxSizing: "border-box",
  },
  header: {
    marginBottom: "24px",
  },
  pageTitle: {
    margin: 0,
    fontSize: "32px",
    fontWeight: 600,
  },
};

export default AdminLayout;