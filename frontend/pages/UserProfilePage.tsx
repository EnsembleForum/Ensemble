import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { userView } from "../interfaces";

interface Props {
  userId: number;
}

const Layout = styled.div`
  padding: 30px;
`

const UserProfilePage = (props: Props) => {
  const userList : userView[] = [
    {
      name_first: "dude", name_last: "bruh",username:  "wow", email: "ggz@gmail.com", user_id: 0
    },
    {
      name_first: "dude", name_last: "bruh",username:  "wow", email: "ggz@gmail.com", user_id: 1
    }
  ]
  const user = userList[props.userId];
  return (
    <Layout>
      <h3>{user.name_first} {user.name_last}</h3>
      <h4>Username: {user.email}</h4>
      <h4>Email: {user.email}</h4>
    </Layout>
  );
};

export default UserProfilePage;