import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { ApiFetch } from "../App";
import { APIcall, queueList } from "../interfaces";
import Navbar from "./components/Navbar";

interface Props { }


const TaskboardPage = (props: Props) => {
  const [queueList, setQueueList] = React.useState<queueList>();
  const call : APIcall = { 
    method: "GET",
    path: "taskboard/queue_list"
  }
  ApiFetch(call).then((data) => {
    console.log(data);
    const out = data as queueList;
    console.log("fetched:", out);
    setQueueList(out);
  });
  if (queueList) {
    return (
      <>
        <Navbar page="taskboard" />
        Taskboard
      </>
    );
  } else {
    return (
      <>
        <Navbar page="taskboard" />
        Loading...
      </>
    )
  }
};

export default TaskboardPage;