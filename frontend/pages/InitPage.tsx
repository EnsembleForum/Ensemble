import styled from "@emotion/styled";
import React from "react";
import { Box, Label, Input, Select } from "theme-ui";
import { ApiFetch } from "../App";
import { Prettify } from "../global_functions";
import { initSchema, loginForm } from "../interfaces";
import { StyledButton } from "./GlobalProps";


interface Props {}

const LoginLayout = styled.body`
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
const InitPage = (props: Props) => {
  const [initDetails, setInitDetails] = React.useState<initSchema>({
    address: '',
    request_type: "POST",
    username_param: '',
    password_param: '',
    success_regex: '',
    username: '',
    password: '',
    email: '', 
    name_first: '',
    name_last: ''
  });
  const onSubmit = (e: { preventDefault: () => void; }) => {
      e.preventDefault();
      // Here we would call api, which would reroute
      ApiFetch("POST", "admin/init", null, initDetails);
      console.log(initDetails);
  } 
  return (
    <LoginLayout>
      <StyledForm as="form" onSubmit={onSubmit}>
        {Object.keys(initDetails).map((eachKey) => {
          if (eachKey === "password") {
            return (
              <>
                <Label htmlFor="password">Password</Label>
                <Input type="password" name="password" id="password" mb={3} onChange={(e) => setInitDetails(initDetails=>({...initDetails, password: e.target.value}))}/>
              </>
            )
          }
          if (eachKey === "request_type") {
            return (
              <>
                <Label htmlFor={eachKey}>Request Type</Label>
                <Select name="request_type" id="request_type" mb={3} value = {initDetails.request_type} onChange={(e) => setInitDetails(initDetails=>({...initDetails, request_type: e.target.value}))}> 
                  <option value = "POST">POST</option>
                  <option value = "GET">GET</option>
                </Select>
              </>
            )
          }
          return (
            <>
              <Label htmlFor={eachKey}>{Prettify(eachKey)}</Label>
              <Input type="text" name={eachKey} id={eachKey} mb={3} onChange={(e) => setInitDetails(initDetails=>({...initDetails, [eachKey]: e.target.value}))} />
            </>
          )
        })}
        <StyledButton type="submit">Submit</StyledButton>
      </StyledForm>
    </LoginLayout>
  );
};

export default InitPage;