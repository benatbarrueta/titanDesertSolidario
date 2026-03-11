import React, { useEffect, useState } from "react";
import AdminLayout from "../components/AdminLayout";
import { adminApiClient } from "../api/adminApiClient";

const StatCard = ({ label, value }) => (
  <div style={styles.card}>
    <div style={styles.cardLabel}>{label}</div>
    <div style={styles.cardValue}>{value}</div>
  </div>
);

const AdminDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    adminApiClient
      .getDashboard()
      .then((res) => {
        setData(res);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Error loading dashboard");
        setLoading(false);
      });
  }, []);

  return (
      <AdminLayout>
      {loading && <p>Cargando dashboard...</p>}
      {error && <p style={{ color: "#ff8b8b" }}>Error: {error}</p>}

      {!loading && !error && data && (
        <>
          <div style={styles.grid}>
            <StatCard label="Total Raised" value={`${data.total_raised} €`} />
            <StatCard label="Participations" value={data.total_participations} />
            <StatCard label="Challenges" value={data.total_challenges} />
            <StatCard label="Active Challenges" value={data.active_challenges} />
            <StatCard label="Published Stages" value={data.published_stages} />
            <StatCard label="Open Stages" value={data.open_stages} />
          </div>

          <div style={styles.twoCols}>
            <div style={styles.panel}>
              <h2 style={styles.panelTitle}>Top Challenges</h2>
              {data.top_challenges?.length ? (
                <ul style={styles.list}>
                  {data.top_challenges.map((item) => (
                    <li key={item.challenge_id} style={styles.listItem}>
                      <strong>{item.challenge_title}</strong>
                      <div>{item.total_amount} €</div>
                      <div>{item.participations_count} participations</div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Sin datos todavía.</p>
              )}
            </div>

            <div style={styles.panel}>
              <h2 style={styles.panelTitle}>Top Warriors</h2>
              {data.top_warriors?.length ? (
                <ul style={styles.list}>
                  {data.top_warriors.map((item) => (
                    <li key={item.warrior_id} style={styles.listItem}>
                      <strong>{item.warrior_name}</strong>
                      <div>{item.raised} €</div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>Sin datos todavía.</p>
              )}
            </div>
          </div>
        </>
      )}
    </AdminLayout>
  );
};

const styles = {
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))",
    gap: "16px",
    marginBottom: "24px",
  },
  card: {
    background: "#151515",
    border: "1px solid #222",
    borderRadius: "16px",
    padding: "20px",
  },
  cardLabel: {
    color: "#aaa",
    fontSize: "14px",
    marginBottom: "10px",
  },
  cardValue: {
    fontSize: "28px",
    fontWeight: 700,
    color: "#E0B07A",
  },
  twoCols: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "20px",
  },
  panel: {
    background: "#151515",
    border: "1px solid #222",
    borderRadius: "16px",
    padding: "20px",
  },
  panelTitle: {
    marginTop: 0,
    marginBottom: "16px",
  },
  list: {
    listStyle: "none",
    padding: 0,
    margin: 0,
  },
  listItem: {
    padding: "12px 0",
    borderBottom: "1px solid #222",
  },
};

export default AdminDashboard;