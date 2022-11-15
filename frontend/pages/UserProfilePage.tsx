import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { Input } from "theme-ui";
import { ApiFetch, getCurrentUser } from "../App";
import { Prettify } from "../global_functions";
import { APIcall, userView } from "../interfaces";
import Navbar from "./components/Navbar";
import { StyledButton } from "./GlobalProps";

interface Props {}

const Layout = styled.div`
  height: 90vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
`
const Profile = styled.div`
  width: 30vw;
  border: 1px solid black;
  padding: 0px 20px 0px 20px;
  border-radius: 10px;
  * {
    font-weight: 300;
    width: 100%;
  }
  h3 {
    font-weight: 500;
    margin: 10px 0 10px 0;
  }
  input {
    margin-bottom: 10px;
  }
  h1 {
    text-align: center;
  }
`
const Row = styled.div`
  width: 100%;
  display: flex;
  h3 {
    width: 10vw;
  }
`

const StyledInput = styled(Input)`
  border-radius: 10px 0 0 10px;
  height: 40px;
  width: 30vw;
`
const SubmitButton = styled(StyledButton)`
  border: 1px solid black;
  border-radius: 0;
  border-left: 0;
  max-width: 7vw;
  height: 40px;
  padding: 0;
`
const CloseButton = styled(SubmitButton)`
  border-radius: 0px 10px 10px 0px;
  max-width: 2vw;
`
const Edit = styled(Row)`
  button {
    flex-grow: 1
  }
`
const EditButton = styled.span`
  border-radius: 3px;
  margin-left: 5px;
  padding: 3px;
  &:hover {
    cursor: pointer;
    background-color: lightgrey;
  }
`

const UserProfilePage = (props: Props) => {
  const [user, setUser] = React.useState<userView>();
  const [update, setUpdate] = React.useState<boolean>(false);
  const [toggle, setToggle] = React.useState<{[key: string]: boolean}>({
    "name_first": false, 
    "name_last": false, 
    "pronouns" : false,
    "email" : false,
  });
  function edit(key : string) {
    const routes : {[key: string] : string} = {
      "name_first": "user/profile/edit_name_first", 
      "name_last": "user/profile/edit_name_last", 
      "pronouns" : "user/profile/edit_pronouns",
      "email" : "user/profile/edit_email",
    }
    const call : APIcall = {
      method: "PUT",
      path: routes[key],
      body: {user_id: getCurrentUser().user_id}
    }
    if (user) {
      call.body[key] = user[key];
      ApiFetch(call).then(() => setUpdate(!update));
    }
    const copy = {...toggle};
    copy[key] = false;
    setToggle(copy);
  }

  React.useEffect(() => {
    const call : APIcall = {
      path: "user/profile",
      method: "GET",
      params: {'user_id': getCurrentUser().user_id.toString()}
    }
    ApiFetch(call).then((data) => {
      setUser(data as userView);
    })
  }, [update]);
  const exclude = ["permission_group", "user_id", "username"]
  if (user) {
    return (
      <div>
        <Navbar page="profile"/>
        <Layout>
          <Profile>
            <h1>Your account</h1>
            <h3>Username: {user.username}</h3>
            <h3>User Group: {user.permission_group}</h3>
            { Object.keys(user).filter(key => !exclude.includes(key)).map((key) => {
              return (
                <>
                  {toggle[key] ? 
                    <>
                      <h3>{Prettify(key)}: </h3>
                      <Edit>
                        <StyledInput value={user[key]} onChange = {((e) => {
                          const copy = {...user};
                          copy[key] = e.target.value;
                          setUser(copy);
                        })}></StyledInput>
                        <SubmitButton onClick={() => edit(key)}>Change</SubmitButton>
                        <CloseButton onClick={() => {
                          const copy = {...toggle};
                          copy[key] = false;
                          setToggle(copy);
                        }}>X</CloseButton>
                      </Edit>
                    </>
                  :
                  <>
                    <h3>
                      {Prettify(key)}: {user[key]} 
                      <EditButton onClick={() => {
                          const copy = {...toggle};
                          copy[key] = true;
                          setToggle(copy);
                        }}>✏️</EditButton>
                    </h3>
                  </>
                  }
                </>
              )
            })
            }
          </Profile>
        </Layout>
      </div>
    );
  } else {
    return (
      <div>
        <Navbar page="profile"/>
      </div>
    )
  }
  
};

export default UserProfilePage;