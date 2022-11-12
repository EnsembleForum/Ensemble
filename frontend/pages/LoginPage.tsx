import styled from "@emotion/styled";
import { stripBasename } from "@remix-run/router";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { IconButton, Text, Box, Label, Input, Checkbox, Select, Textarea, Flex, Button, } from "theme-ui";
import { ApiFetch, setToken } from "../App";
import { APIcall, initReturn, loginForm } from "../interfaces";
import Navbar from "./components/Navbar";
import { StyledButton } from "./GlobalProps";
import UserContext from "./userContext";
import PermissionsContext from "./userContext";


interface Props { }

const LoginLayout = styled.div`
  height: 90vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const StyledForm = styled(Box)`
  border: 1px solid black;
  padding: 10px;
  border-radius: 2%;
`;
const LoginPage = (props: Props) => {
  const { currentUser, setCurrentUser } = React.useContext(UserContext);
  const navigate = useNavigate();
  const [loginDetails, setLoginDetails] = React.useState<loginForm>({
    username: '',
    password: '',
  });
  const onSubmit = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    // Here we would call api, which would reroute
    const api: APIcall = {
      method: "POST",
      path: "auth/login",
      body: loginDetails
    }
    ApiFetch(api)
      .then((data) => {
        const check = data as initReturn;
        setToken(check.token);
        setCurrentUser({user_id: check.user_id, permissions: check.permissions})
        navigate("/browse");
      })
  }
  return (
    <>
    <Navbar page={"login"}/>
    <LoginLayout>
      <StyledForm as="form" onSubmit={onSubmit}>
        <Label htmlFor="username">Username</Label>
        <Input type="text" name="username" id="username" mb={3} onChange={(e) => setLoginDetails(loginDetails => ({ ...loginDetails, username: e.target.value }))} />
        <Label htmlFor="password">Password</Label>
        <Input type="password" name="password" id="password" mb={3} onChange={(e) => setLoginDetails(loginDetails => ({ ...loginDetails, password: e.target.value }))} />
        <StyledButton type="submit">Submit</StyledButton>
      </StyledForm>
    </LoginLayout>
    </>
  );
};

export default LoginPage;
