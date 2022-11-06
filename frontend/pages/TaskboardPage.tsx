import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import Navbar from "./components/Navbar";

interface Props { }

const TaskboardPage = (props: Props) => {
  return (
    <>
      <Navbar page="taskboard" />
      Taskboard
    </>
  );
};

export default TaskboardPage;