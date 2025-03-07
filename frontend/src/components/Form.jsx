import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/Form.css";

function Form({ route, method }) {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const payload = { email, password };

      if (method === "register") {
        payload.username = username;
      }

      // Send request to route
      const res = await api.post(route, payload);
      if (method === "login") {
        console.log("we logging in");
        localStorage.setItem(ACCESS_TOKEN, res.data.token.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.token.refresh);
        navigate("/home");
      } else {
        navigate("/login");
      }
    } catch (error) {
      alert(error);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>{method}</h1>

      <input
        className="form-email"
        type="text"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />

      {method == "register" && (
        <input
          className="form-input"
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
        />
      )}

      <input
        className="form-input"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />

      <button className="form-button" type="submit">
        {method}
      </button>
    </form>
  );
}

export default Form;
