import { Navigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import { useState, useEffect } from "react";

function ProtectedRoute({ children }) {
  const [isAuthorised, setIsAuthorized] = useState(null);

  useEffect(() => {
    auth();
  }, []);

  const refreshToken = async () => {
    try {
      const refreshToken = localStorage.getItem(REFRESH_TOKEN);

      const res = await api.post(
        "/refresh",
        {},
        {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
          },
        }
      );

      if (res.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        setIsAuthorized(true);
      } else {
        setIsAuthorized(false);
      }

    } catch (err) {
      console.error("Error while refreshing access token:", err);
      setIsAuthorized(false);
    }
  };

  const auth = async () => {
    try {
      const token = localStorage.getItem(ACCESS_TOKEN);

      if (!token) {
        setIsAuthorized(false);
        return;
      }

      const decoded = jwtDecode(token);
      const tokenExpiration = decoded.exp;
      const currentTime = Date.now() / 1000;

      if (tokenExpiration < currentTime) {
        await refreshToken();
      } else {
        setIsAuthorized(true);
      }

    } catch (err) {
      console.error("Error while authenticating:", err);
      setIsAuthorized(false);
      
    }
  };

  if (isAuthorised === null) {
    return <div>Loading....</div>;
  }

  return isAuthorised ? children : <Navigate to="/login" />;
}

export default ProtectedRoute;
