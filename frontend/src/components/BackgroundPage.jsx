import { Flex } from "@chakra-ui/react";

function BackgroundPage({ children }) {
  return (
    <Flex
      minHeight="100vh"
      width="full"
      align="center"
      justifyContent="center"
      backgroundColor={"#F3F4F6"}
    >
      {children}
    </Flex>
  );
}

export default BackgroundPage;
