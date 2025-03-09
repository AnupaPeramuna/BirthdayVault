import { useNavigate } from "react-router-dom";
import {
  Box,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
} from "@chakra-ui/react";
import useForm from "../hooks/useForm";
import BackgroundPage from "./BackgroundPage";
import formConfig from "../config/formConfig";
import api from "../api";

function Form({ formName, route, payload, onSubmit }) {
  const navigate = useNavigate();

  // Initialize each field in the payload to an empty string
  const initialState = payload.reduce((acc, field) => {
    acc[field] = "";
    return acc;
  }, {});

  const [formData, setFormData] = useForm({ ...initialState });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formResponse = await api.post(route, formData);
      onSubmit(formResponse.data);
    } catch (error) {
      alert(error);
      navigate("/register");
    }
  };

  const generateFormFields = () => {
    const inputWidth = "30rem";

    return payload.map((formField, index) => {
      if (!formConfig[formField]) {
        return;
      }

      const { label, name, type, placeholder, autoComplete } =
        formConfig[formField];

      return (
        <FormControl key={index}>
          <FormLabel>{label}</FormLabel>
          <Input
            name={name}
            type={type}
            placeholder={placeholder}
            onChange={setFormData}
            autoComplete={autoComplete ? name : "off"}
            maxWidth={inputWidth}
            width="100%"
          />
        </FormControl>
      );
    });
  };

  return (
    <BackgroundPage>
      <Box
        borderWidth={1}
        px={4}
        width="100%"
        maxWidth="600px"
        borderRadius={4}
        textAlign="center"
        boxShadow="xl"
        backgroundColor={"white"}
      >
        <Box textAlign="center" marginTop={"2rem"}>
          <Heading>{formName}</Heading>
        </Box>
        <Box p={5}>
          <Box my={8} textAlign="left">
            <form onSubmit={handleSubmit}>
              {generateFormFields()}
              <Button width="full" mt={4} type="submit" color={"#1E3A8A"}>
                {formName}
              </Button>
            </form>
          </Box>
        </Box>
      </Box>
    </BackgroundPage>
  );
}

export default Form;
