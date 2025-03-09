import { useNavigate } from "react-router-dom";
import Form from "../components/Form";

function Register() {
  const navigate = useNavigate();
  return (
    <Form
      formName="Sign Up"
      route="/auth/register"
      payload={["email", "username", "password"]}
      onSubmit={() => {
        navigate("/login");
      }}
    />
  );
}

export default Register;
