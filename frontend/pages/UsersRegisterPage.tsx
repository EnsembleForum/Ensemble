import styled from "@emotion/styled";
import { stripBasename } from "@remix-run/router";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { IconButton, Text, Box, Label, Input, Checkbox, Select, Textarea, Flex, Button, } from "theme-ui";
import { ApiFetch } from "../App";
import { Prettify } from "../global_functions";
import { APIcall, loginForm, usersRegister, userToAdd } from "../interfaces";
import { StyledButton } from "./GlobalProps";


interface Props { }

const LoginLayout = styled.div`
  height: 90vh;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
`;

const StyledForm = styled(Box)`
  border: 1px solid black;
  padding: 10px;
  border-radius: 2%;
  p {
    margin: 0 0 5px 0;
  }
`;

const StyledButtons = styled(Box)`
  display: flex;
  justify-content: space-evenly;
`;

const StyledTable = styled.table`
  margin-top: 50px;
  border: 1px solid black;
  border-radius: 2px;
  border-spacing:0;
  border-collapse: collapse; 
  width: 50%;
  * {
    border: 1px solid black;
    padding: 5px;
  }
  tr > th {
    background-color: grey;
  }
  &:nth-child(3) {
    background-color: lightgrey;
  }
`;


const UsersRegisterPage = (props: Props) => {
  const navigate = useNavigate();
  const defaultState: userToAdd = {
    name_first: '',
    name_last: '',
    email: '',
    username: '',
  };
  const permissions = ["admin", "moderator", "user"]
  const [registerList, setRegisterList] = React.useState([] as userToAdd[]);
  const [registerDetails, setRegisterDetails] = React.useState<userToAdd>(defaultState);
  const [groupPermission, setGroupPermission] = React.useState(3);
  // 1 admin, 2 mod, 3 students
  const onSubmit = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    // Here we would call api, which would reroute
    const postObject: usersRegister = { users: registerList, group_id: groupPermission };
    const api: APIcall = {
      method: "POST",
      path: "admin/users/register",
      body: postObject,
    }
    ApiFetch(api)
      .then((data) => {
        void data;
        setRegisterList([]);
        navigate("/admin");
      })
  }
  const resetGroupPermission = (e: { preventDefault: () => void; target: { value: string; }; }) => {
    e.preventDefault();
    setGroupPermission(parseInt(e.target.value));
    setRegisterDetails(defaultState);
  }
  const resetUser = (e: { preventDefault: () => void; }) => {
    e.preventDefault();
    setRegisterList(registerList => [...registerList, registerDetails]);
    setRegisterDetails(defaultState);
  }
  return (
    <LoginLayout>
      <StyledForm id="test" as="form" onSubmit={onSubmit}>
        <Label>Permission Group</Label>
        <p><small>Changing permission group will reset user list</small></p>
        <Select name="permission" id="permission" mb={3} value={groupPermission} onChange={resetGroupPermission}>
          <option value="1">1: Admin</option>
          <option value="2">2: Moderator</option>
          <option value="3">3: User</option>
        </Select>
        {Object.keys(registerDetails).map((eachKey) => {
          return (
            <>
              <Label htmlFor={eachKey} key={eachKey}>{Prettify(eachKey)}</Label>
              <Input type="text" key={eachKey + "e"} name={eachKey} id={eachKey} mb={3} value={registerDetails[eachKey]} onChange={(e) => setRegisterDetails(registerDetails => ({ ...registerDetails, [eachKey]: e.target.value }))} />
            </>
          )
        })}
        <StyledButtons>
          <StyledButton onClick={resetUser}>Add {permissions[groupPermission - 1]}</StyledButton>
          <StyledButton type="submit">Submit</StyledButton>
        </StyledButtons>
      </StyledForm>

      <StyledTable>
        <tr>
          {Object.keys(registerDetails).map((eachKey) => {
            return (
              <th>{Prettify(eachKey)}</th>
            )
          })}
        </tr>
        {registerList.map((user) => {
          return (
            <tr>
              {Object.keys(user).map((eachKey) => {
                return (
                  <td>
                    {user[eachKey]}
                  </td>
                )
              })
              }
            </tr>
          )
        })
        }
      </StyledTable>
    </LoginLayout>
  );
};

export default UsersRegisterPage;