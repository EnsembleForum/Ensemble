import styled from "@emotion/styled";
import React, { useEffect } from "react";
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
    <Content>
      {pages[currPage]}
    </Content>
  )
};

export default MainPage;