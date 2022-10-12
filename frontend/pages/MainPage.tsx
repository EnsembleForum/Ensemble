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

const Navbar = styled.ul`
  height: 50px;
  width: 100%;
  display: flex;
  align-items: center;
  padding: 10px;
  * {
    padding: 10px;
    margin: 10px;
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
    <>
      <Navbar as="nav">
        <a onClick={(e) => {setCurrPage("browse")}}>browse</a>
        <a onClick={(e) => {setCurrPage("taskboard")}}>taskboard</a>
      </Navbar>
      {page}
    </>
  )
};

export default MainPage;