import styled from "@emotion/styled";
import React from "react";
import { useNavigate } from "react-router-dom";
import { Box, Label, Input, Select } from "theme-ui";
import { ApiFetch, setToken } from "../App";
import { Prettify } from "../global_functions";
import { APIcall, initReturn, initSchema, loginForm } from "../interfaces";
import { StyledButton } from "./GlobalProps";

interface Props { }

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
const InitPage = (props: Props) => {
  const navigate = useNavigate();
  const [initDetails, setInitDetails] = React.useState<initSchema>({
    address: 'http://localhost:5812/login',
    request_type: "get",
    username_param: 'username',
    password_param: 'password',
    success_regex: 'true',
    username: 'admin1',
    password: 'admin1',
    email: 'admin@example.com',
    name_first: 'Robin',
    name_last: 'Banks'
  });
  const onSubmit = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    // Here we would call api, which would reroute
    const api: APIcall = {
      method: "POST",
      path: "admin/init",
      body: initDetails
    }
    ApiFetch(api)
      .then((data) => {
        const check = data as initReturn;
        setToken(check.token)
        navigate("/main");
      });
  }
  return (
    <LoginLayout>
      <StyledForm as="form" onSubmit={onSubmit}>
        {Object.keys(initDetails).map((eachKey) => {
          if (eachKey === "password") {
            return (
              <>
                <Label htmlFor="password">Password</Label>
                <Input type="password" name="password" id="password" value={initDetails[eachKey]} mb={3} onChange={(e) => setInitDetails(initDetails => ({ ...initDetails, password: e.target.value }))} />
              </>
            )
          }
          if (eachKey === "request_type") {
            return (
              <>
                <Label htmlFor={eachKey}>Request Type</Label>
                <Select name="request_type" id="request_type" mb={3} value={initDetails.request_type} onChange={(e) => setInitDetails(initDetails => ({ ...initDetails, request_type: e.target.value }))}>
                  <option value="post">POST</option>
                  <option value="get">GET</option>
                </Select>
              </>
            )
          }
          return (
            <>
              <Label htmlFor={eachKey}>{Prettify(eachKey)}</Label>
              <Input type="text" name={eachKey} id={eachKey} mb={3} value={initDetails[eachKey]} onChange={(e) => setInitDetails(initDetails => ({ ...initDetails, [eachKey]: e.target.value }))} />
            </>
          )
        })}
        <StyledButton type="submit">Submit</StyledButton>
      </StyledForm>
    </LoginLayout>
  );
};

export default InitPage;