import React, { useEffect, useState } from "react";
import AdminLayout from "../components/AdminLayout";
import { adminApiClient } from "../api/adminApiClient";

const AdminParticipations = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    adminApiClient
      .getParticipations()
      .then((res) => {
        setItems(Array.isArray(res) ? res : []);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Error loading participations");
        setLoading(false);
      });
  }, []);

  return (
      <AdminLayout>
      {loading && <p>Cargando participations...</p>}
      {error && <p style={{ color: "#ff8b8b" }}>Error: {error}</p>}

      {!loading && !error && (
        <div style={styles.tableWrapper}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>ID</th>
                <th style={styles.th}>Participant</th>
                <th style={styles.th}>Email</th>
                <th style={styles.th}>Challenge</th>
                <th style={styles.th}>Option</th>
                <th style={styles.th}>Amount</th>
                <th style={styles.th}>Status</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id}>
                  <td style={styles.td}>{item.id}</td>
                  <td style={styles.td}>{item.participant_name}</td>
                  <td style={styles.td}>{item.email}</td>
                  <td style={styles.td}>{item.challenge_title_at_time}</td>
                  <td style={styles.td}>{item.option_name_at_time}</td>
                  <td style={styles.td}>{item.amount} €</td>
                  <td style={styles.td}>{item.payment_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </AdminLayout>
  );
};

const styles = {
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
  },
};

export default AdminParticipations;