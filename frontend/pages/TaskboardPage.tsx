import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { ApiFetch, getPermission } from "../App";
import { APIcall, postView, queueList, queueListPosts } from "../interfaces";
import { theme } from "../theme";
import Navbar from "./components/Navbar";
import QueueView from "./components/QueueView";
import { StyledButton } from "./GlobalProps";
import QueueContext, { UpdateContext } from "./queueContext";
import ReactTooltip from 'react-tooltip';
import { Box, Input, Label } from "theme-ui";

interface Props { }

const StyledLayout = styled.div`
  width: 100vw;
  max-width: 100vw;
  min-width: 100vw;
  height: 90vh;
  display: flex;
  flex-direction: row;
  overflow: hidden;
`
const Layout = styled.span`
  overflow: hidden;
`
const StyledQueues = styled.div`
  width: 60vw;
  height: 82vh;
  padding: 30px;
  overflow:auto;
  h2 {
    height: 7vh;
    margin: 0;
    font-weight: 300;
  }  
`
const StyledViewOnlyQueues = styled(StyledQueues)`
  width: 40vw;
  background-color: ${theme.colors?.muted};
`
const QueueCols = styled.div`
  display: flex;
  flex-direction: row;
`

const NewButton = styled(StyledButton)`
  min-width: 30px;
  max-height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  font-size: 30px;
  background-color: green;
`

const StyledForm = styled(Box)`
  border: 3px dashed darkgrey;
  padding: 10px;
  border-radius: 2%;
  min-width: 300px;
`;

const TaskboardPage = (props: Props) => {
  const [queueList, setQueueList] = React.useState<queueListPosts[]>();
  const [update, setUpdate] = React.useState<boolean>(false);
  const [toggleCreate, setToggleCreate] = React.useState<boolean>(false);
  const [queueName, setQueueName] = React.useState<string>();

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

  async function createQueue() {
    const createQueueCall : APIcall = { 
      method: "POST",
      path: "taskboard/queue_list/create",
      body: {queue_name: queueName}
    }
    await ApiFetch(createQueueCall);
    setToggleCreate(false);
    setUpdate(!update);
  }

  React.useEffect(() => {
    getQueues();
  },[update])

  const createForm = (
    <>
    <StyledForm>
      <Input type="text" placeholder="Name" name="username" id="username" mb={3} onChange={(e) => setQueueName(e.target.value)} />
      <StyledButton style = {{width: "83%", marginRight: "2%"}} onClick={createQueue}>Create Queue</StyledButton>
      <StyledButton style = {{width: "15%"}} onClick={() => setToggleCreate(false)}>X</StyledButton>
    </StyledForm>
    </>
  )

  if (queueList) {
    return (
      <QueueContext.Provider value = {{queueList, setQueueList}}>
      <UpdateContext.Provider value = {{update, setUpdate}}>
        <Layout>
          <Navbar page="taskboard" />
          <StyledLayout>
            <StyledQueues>
              <h2>Queues</h2>
              <QueueCols>
                { queueList.filter(queue => !queue.view_only).map((queue) => {
                  return (
                    <QueueView queue={queue}></QueueView>
                  )
                })}
                {getPermission(23) ? ( toggleCreate ? 
                createForm
                 :
                <span style={{display: "flex", flexDirection: "column", justifyContent: "center"}}>
                  <ReactTooltip place="top" type="dark" effect="solid"/>
                  <NewButton data-tip="Create a new queue" onClick={ () => setToggleCreate(true)}>+</NewButton>
                </span>
                ) : <></>}
                <div style={{minWidth: "30px"}}></div>
              </QueueCols>
            </StyledQueues>
            <StyledViewOnlyQueues>
              <h2>Answered, Closed, Deleted and Reported Posts</h2>
              <QueueCols>
              { queueList.filter(queue => queue.view_only).map((queue) => {
                return (
                  <QueueView queue={queue}></QueueView>
                )
              })}
                <div style={{minWidth: "30px"}}></div>
              </QueueCols>
            </StyledViewOnlyQueues>
          </StyledLayout>
        </Layout>
        </UpdateContext.Provider>
      </QueueContext.Provider>
    );
  } else {
    return (
      <>
        <Navbar page="taskboard" />
        <div style={{padding: "30px"}}> Loading... </div>
      </>
    )
  }
};

export default TaskboardPage;