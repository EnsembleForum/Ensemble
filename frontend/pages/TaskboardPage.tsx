import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { ApiFetch } from "../App";
import { APIcall, postView, queueList, queueListPosts } from "../interfaces";
import Navbar from "./components/Navbar";
import QueueView from "./components/QueueView";

interface Props { }

const StyledLayout = styled.div`
  width: 100vw;
  height: 90vh;
  display: flex;
  flex-direction: row;
  * > h2 {
    height: 10vh;
    margin: 0;
    font-weight: 300;
  }
`

const StyledQueues = styled.div`
  width: 60vw;
  height: 90vh;
  padding: 30px;
  display: flex;
  flex-direction: column;
`
const StyledViewOnlyQueues = styled.div`
  width: 40vw;
  height: 90vh;
  background-color: lightgrey;
  padding: 30px;
  display: flex;
  flex-direction: column;
  div {
    display: flex;
    flex-direction: row;
  }
`

const TaskboardPage = (props: Props) => {
  const [queueList, setQueueList] = React.useState<queueListPosts[]>();
  const [updateQueues, setUpdateQueues] = React.useState<boolean>(false);
  async function getQueues() {
    const queueCall : APIcall = { 
      method: "GET",
      path: "taskboard/queue_list"
    }
    const queues = await ApiFetch(queueCall) as queueList;

    let queuesWithPosts : queueListPosts[] = [];
    for (const queue of queues.queues) {
      const call : APIcall = {
        method: "GET",
        path: "taskboard/queue/post_list",
        params: {"queue_id": queue.queue_id.toString()}
      }
      const queueWithPosts = await (ApiFetch(call)) as queueListPosts;
      queuesWithPosts.push(queueWithPosts);
    }
    for (const queue of queuesWithPosts) {
      let postsToFetch : postView[] = [];
      for (const postId of queue.posts) {
        const postCall: APIcall = {
          method: "GET",
          path: "browse/post_view",
          params: { "post_id": postId.toString() }
        }
        const post = await ApiFetch(postCall) as postView;
        postsToFetch.push(post);
      }
      queue.posts = postsToFetch;
    }
    setQueueList(queuesWithPosts);
  }

  React.useEffect(() => {
     getQueues();
  },[])

  if (queueList) {
    return (
      <>
        <Navbar page="taskboard" />
        <StyledLayout>
          <StyledQueues>
            <h2>Queues</h2>
            <div>
              { queueList.filter(queue => !queue.view_only).map((queue) => {
                return (
                  <QueueView queue={queue}></QueueView>
                )
              })}
            </div>
          </StyledQueues>
          <StyledViewOnlyQueues>
            <h2>Closed and Answered</h2>
            { queueList.filter(queue => queue.view_only).map((queue) => {
          return (
            <>{queue.queue_name} {queue.queue_id}</>
          )
        })}
          </StyledViewOnlyQueues>
        </StyledLayout>
        
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