import React from "react";
import { queueListPosts } from "../interfaces";

export const UpdateContext = React.createContext({
  update: false,
  setUpdate: (active:boolean) => {}
}); 

// set the defaults
const defaultQueueList:queueListPosts[] =  [];
const QueueContext = React.createContext({
  queueList: defaultQueueList,
  setQueueList: (active:queueListPosts[]) => {}
});

export default QueueContext;

