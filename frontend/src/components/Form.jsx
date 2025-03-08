import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import {
  Box,
  Flex,
  Heading,
  FormControl,
  FormLabel,
  Input,
  Button,
} from "@chakra-ui/react";

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
    <Flex
      minHeight="100vh"
      width="full"
      align="center"
      justifyContent="center"
      backgroundColor={"#F3F4F6"}
    >
      <Box
        borderWidth={1}
        px={4}
        width="full"
        maxWidth="500px"
        borderRadius={4}
        textAlign="center"
        boxShadow="xl"
        backgroundColor={"white"}
      >
        <Box textAlign="center" marginTop={"2rem"}>
          <Heading>{method}</Heading>
        </Box>
        <Box p={4}>
          <Box my={8} textAlign="left">
            <form onSubmit={handleSubmit}>
              <FormControl>
                <FormLabel>Email address</FormLabel>
                <Input
                  type="email"
                  placeholder="Enter your email address"
                  onChange={(e) => setEmail(e.target.value)}
                  autoComplete="email"
                  maxWidth="25rem"
                  width="100%"
                />
              </FormControl>

              {method === "register" && (
                <FormControl mt={4}>
                  <FormLabel>Username</FormLabel>
                  <Input
                    type="text"
                    placeholder="Enter your username"
                    onChange={(e) => setUsername(e.target.value)}
                    autoComplete="username"
                    maxWidth="25rem"
                    width="100%"
                  />
                </FormControl>
              )}

              <FormControl mt={4}>
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  placeholder="Enter your password"
                  onChange={(e) => setPassword(e.target.value)}
                  maxWidth="25rem"
                  width="100%"
                />
              </FormControl>

              <Button width="full" mt={4} type="submit" color={"#1E3A8A"}>
                {method}
              </Button>
            </form>
          </Box>
        </Box>
      </Box>
    </Flex>
  );
}

export default Form;
