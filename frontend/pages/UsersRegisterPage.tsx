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

const Layout = styled.div`
  height: 80vh;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
`;

const StyledForm = styled(Box)`
  width: 30vw;
  margin-top: 5vh;
  height: 60vh;
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
  * {
    height: 60px;
    margin: 5px;
  }
`;

const StyledTable = styled.div`
  margin-top: 5vh;
  width: 56vw;
  padding: 10
  background-colour: lightgrey;
  border-radius: 10px;
  border: 2px solid grey;
  height: 60vh;
  * {
    text-align: center;
  }
  overflow: auto;

`;
const Row = styled.div`
  width: 56vw;
  height: 5vh;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  border-bottom: 1px solid grey;
  font-weight: 700;
`

const Col = styled.div`
  width: 10vw;
`


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
    <Layout>
      <StyledForm id="test" as="form" onSubmit={onSubmit}>
        <Label>Permission Group</Label>
        <p><small>Changing permission group will reset user list</small></p>
        <Select name="permission" id="permission" mb={3} value={groupPermission} onChange={resetGroupPermission}>
          <option value="1">1: Admin</option>
          <option value="2">2: Moderator</option>
          <option value="3">3: User</option>
        </Select>
        {Object.keys(registerDetails).map((eachKey) => {
          console.log(eachKey);
          return (
            <Input 
              type="text" 
              key={eachKey} 
              placeholder={Prettify(eachKey)} 
              name={eachKey} 
              id={eachKey} 
              mb={3} 
              value={registerDetails[eachKey]} 
              onChange={(e) => setRegisterDetails(registerDetails => ({ ...registerDetails, [eachKey]: e.target.value }))} 
            />
          )
        })}
        <StyledButtons>
          <StyledButton onClick={resetUser}>Add {permissions[groupPermission - 1]}</StyledButton>
          <StyledButton onClick={() => {setRegisterDetails(defaultState)}}>Clear {permissions[groupPermission - 1]} Info</StyledButton>
          <StyledButton onClick={() => {setRegisterList([])}}>Clear List</StyledButton>
          <StyledButton type="submit">Submit</StyledButton>
        </StyledButtons>
      </StyledForm>

      <StyledTable>
        <Row style={{backgroundColor: "lightGrey"}}>
          {Object.keys(registerDetails).map((eachKey) => {
            return (
              <Col>{Prettify(eachKey)}</Col>
            )
          })}
        </Row>
        {registerList.map((user) => {
          return (
            <Row>
              {Object.keys(user).map((eachKey) => {
                return (
                  <Col>
                    {user[eachKey]}
                  </Col>
                )
              })
              }
            </Row>
          )
        })
        }
      </StyledTable>
    </Layout>
  );
};

export default UsersRegisterPage;