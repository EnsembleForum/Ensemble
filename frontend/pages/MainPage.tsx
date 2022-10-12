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


interface Props {
  page: "taskboard" | "browse";
}
const Layout = styled.div`
  height: 100%;
`

const Navbar = styled.ul`
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
    border-radius: 10%;
    &:hover {
      cursor: pointer;
      background-color: darkgrey;
    }
  }
  background-color: lightgrey;
`;

const MainPage = (props: Props) => {
  const [currPage, setCurrPage] = React.useState<string>(props.page);
  let page = <BrowsePage/>;
  if (currPage === "taskboard") {
    page = <TaskboardPage/>
  }
  return (
    <Layout>
      <Navbar as="nav">
        <h1>ENSEMBLE</h1>
        <a onClick={(e) => {setCurrPage("browse")}}>Browse</a>
        <a onClick={(e) => {setCurrPage("taskboard")}}>Taskboard</a>
      </Navbar>
      {page}
    </Layout>
  )
};

export default MainPage;