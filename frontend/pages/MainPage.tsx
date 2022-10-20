import styled from "@emotion/styled";
import React from "react";
import { Box, Label, Input, Select, Flex, } from "theme-ui";
import {
  Route,
  NavLink,
  HashRouter
} from "react-router-dom";
import BrowsePage from "./BrowsePage";
import TaskboardPage from "./TaskboardPage";
import AdminPage from "./AdminPage";
import { pageList } from "../interfaces";
import { Prettify } from "../global_functions";


interface Props {
  page: "taskboard" | "browse" | "admin";
}
const Layout = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: 100%;
`

export const Navbar = styled.div`
  height: 60px;
  width: 100vw;
  display: flex;
  align-items: center;
  * {
    padding: 10px;
    margin: 10px;
  }
  a {
    background-color: lightgrey;
    border-radius: 10px;
    min-width: 60px;
    display: flex;
    justify-content: center;
    &:hover {
      cursor: pointer;
      background-color: lightgrey;
      filter: brightness(85%);
    }
  }
  background-color: lightgrey;
`;

const Content = styled.div`

`

const MainPage = (props: Props) => {
  const [currPage, setCurrPage] = React.useState<string>(props.page);
  let pages: pageList = {
    "browse": <BrowsePage />,
    "taskboard": <TaskboardPage />,
    "admin": <AdminPage page={"register_users"} />
  };
  return (
    <Layout>
      <Navbar as="nav">
        <h1>ENSEMBLE</h1>
        {Object.keys(pages).map((key) => {
          return (<a key={key} style={(key === currPage) ? { filter: "brightness(85%)" } : { filter: "brightness(100%)" }} onClick={(e) => { setCurrPage(key) }}>{Prettify(key)}</a>)
        })}
      </Navbar>
      <Content>
        {pages[currPage]}
      </Content>
    </Layout>
  )
};

export default MainPage;