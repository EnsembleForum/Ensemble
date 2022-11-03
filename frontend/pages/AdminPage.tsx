import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { Prettify } from "../global_functions";
import { pageList } from "../interfaces";
import { theme } from "../theme";
import Navbar, { StyledNavbar } from "./components/Navbar";
import InitPage from "./InitPage";
import RegisterPage from "./RegisterPage";
import TaskboardPage from "./TaskboardPage";
import UsersRegisterPage from "./UsersRegisterPage";

interface Props {
  page: "initialise_forum" | "register_users";
}

const AdminPanel = styled(StyledNavbar)`
  background-color: white;
  align-items: center;
  justify-content: center;
  a {
    background-color: ${theme.colors?.highlight};
    border-radius: 10px;
    min-width: 60px;
    display: flex;
    justify-content: center;
    &:hover {
      cursor: pointer;
      background-color: ${theme.colors?.highlight};
      filter: brightness(85%);
    }
    &:active {
      background-color: ${theme.colors?.highlight};
      filter: brightness(85%);
    }
  }
`

const AdminPage = (props: Props) => {
  const [currPage, setCurrPage] = React.useState<string>(props.page);
  let pages: pageList = {
    "initialise_forum": <InitPage />,
    "register_users": <UsersRegisterPage />,
  };
  return (
    <>
      <Navbar page="admin" />
      <AdminPanel>
        {Object.keys(pages).map((key) => {
          let active = '';
          if (key === currPage) {
            active = "active"
          }
          return (<a key={key} style={(key === currPage) ? { filter: "brightness(95%)" } : { filter: "brightness(100%)" }} onClick={(e) => { setCurrPage(key) }}>{Prettify(key)}</a>)
        })}
      </AdminPanel>
      {pages[currPage]}
    </>
  )
};

export default AdminPage;