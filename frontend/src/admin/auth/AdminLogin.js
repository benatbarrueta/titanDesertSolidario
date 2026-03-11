import React from "react";

const AdminLogin = () => {

  const loginWithGoogle = () => {
    window.location.href =
      "http://localhost:8000/api/v1/admin/auth/google";
  };

  return (
    <div className="admin-login">
      <h1>Titan Desert Admin</h1>

      <button onClick={loginWithGoogle}>
        Login with Google
      </button>
    </div>
  );
};

export default AdminLogin;