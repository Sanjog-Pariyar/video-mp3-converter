import { Navigate } from "react-router-dom";
import { getToken } from "../api";
import type { ReactNode } from "react";

interface Props {
  children: ReactNode;
}

const ProtectedRoute = ({ children }: Props) => {
  const token = getToken();
  return token ? children : <Navigate to="/" replace />;
};

export default ProtectedRoute;
