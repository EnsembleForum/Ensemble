import styled from "@emotion/styled";
import { stripBasename } from "@remix-run/router";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { IconButton, Text, Box, Label, Input, Checkbox, Select, Textarea, Flex, Button,  } from "theme-ui";
import { ApiFetch, getToken } from "../App";
import { Prettify } from "../global_functions";
import { APIcall, loginForm, usersRegister, userToAdd } from "../interfaces";
import { StyledButton } from "./GlobalProps";


interface Props {}

const LoginLayout = styled.div`
  height: 100%;
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
  const navigate = useNavigate();
  const defaultState : userToAdd = {
    name_first: '',
    name_last: '',
    email: '',
    username: '',
  };
  const [registerList, setRegisterList] = React.useState([] as userToAdd[]);
  const [registerDetails, setRegisterDetails] = React.useState<userToAdd>(defaultState);
  const onSubmit = (e: { preventDefault: () => void; }) => {
      e.preventDefault();
      // Here we would call api, which would reroute
      const postObject : usersRegister = {users : registerList};
      const api : APIcall = {
        method: "POST",
        path:"admin/users/register",
        body: postObject,
        token: getToken()
      }
      ApiFetch(api)
      .then((data) => {
        void data;
        navigate("main");
      })
  }
  const resetUser = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    setRegisterList(registerList => [...registerList, registerDetails]);
    setRegisterDetails(defaultState);
  }  
  return (
    <LoginLayout>
      <StyledForm id = "test" as="form" onSubmit={onSubmit}>
        {Object.keys(registerDetails).map((eachKey) => {
          return (
            <>
              <Label htmlFor={eachKey}>{Prettify(eachKey)}</Label>
              <Input type="text" name={eachKey} id={eachKey} mb={3} value = {registerDetails[eachKey]} onChange={(e) => setRegisterDetails(registerDetails=>({...registerDetails, [eachKey]: e.target.value}))} />
            </>
          )
        })}        
        <StyledButton onClick={resetUser}>Add another user</StyledButton>
        <StyledButton type="submit">Submit</StyledButton>
      </StyledForm>
    </LoginLayout>
  );
};

export default LoginPage;