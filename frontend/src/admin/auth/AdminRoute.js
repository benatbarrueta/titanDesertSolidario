import { Navigate } from "react-router-dom";
import { useAdminAuth } from "./AdminAuthContext";

const AdminRoute = ({ children }) => {
  const { token } = useAdminAuth();

  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }

  return children;
};

export default AdminRoute;