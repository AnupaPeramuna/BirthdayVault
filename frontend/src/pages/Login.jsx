import { useNavigate } from "react-router-dom";
import Form from "../components/Form";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Login() {
  const navigate = useNavigate();
  return (
    <Form
      formName="Log In"
      route="/auth/login"
      payload={["email", "password"]}
      onSubmit={(data) => {
        localStorage.setItem(ACCESS_TOKEN, data.token.access);
        localStorage.setItem(REFRESH_TOKEN, data.token.refresh);
        navigate("/home");
      }}
    />
  );
}

export default Login;
