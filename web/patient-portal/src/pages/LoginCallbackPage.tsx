import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { signinCallback } from "../hooks/useAuth";

export default function LoginCallbackPage() {
  const navigate = useNavigate();
  useEffect(() => { signinCallback().then(() => navigate("/my")); }, [navigate]);
  return <p>Signing you in...</p>;
}
