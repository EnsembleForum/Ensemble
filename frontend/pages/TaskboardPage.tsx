import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { ApiFetch } from "../App";
import { APIcall, postView, queueList, queueListPosts } from "../interfaces";
import { theme } from "../theme";
import AuthorView from "./components/AuthorView";
import Navbar from "./components/Navbar";
import QueueView from "./components/QueueView";

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


const FlexWrapper = styled.div`
  display: flex;
  flex-direction: column;
  content-align: space-between
`
// Writing styled components
const StyledQueue = styled.div`
  padding: 10px;
  border-radius: 10px;
  background-color: lightgrey;
  width: 300px;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  margin-right: 30px;
`;
const QueueHeader = styled.div`
  display: flex;
  justify-content: space-between;
  h3, h4 {
    padding: 6px 10px 6px 10px;
    margin: 0;
  }
  h4 {
    color: white;
    border-radius: 10px;
    background-color: ${theme.colors?.primary};
  }
`
const QueueItem = styled.div`
  padding: 10px;
  margin-top: 10px;
  background-color: white;
  border-radius: 10px;
  &:hover {
    cursor: pointer;
    filter: brightness(90%);
  }
`
const Heading = styled.span`
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;  
  overflow: hidden;
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
  const navigate = useNavigate();

  if (queueList) {
    return (
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
            </QueueCols>
          </StyledQueues>
          <StyledViewOnlyQueues>
            <h2>Answered, Closed, Deleted and Reported Posts</h2>
            <QueueCols>
            { queueList.filter(queue => queue.view_only).map((queue) => {
              return (
                <FlexWrapper>
                  <StyledQueue>
                    <QueueHeader>
                      <h3>{queue.queue_name}</h3>
                      <h4>{queue.posts.length}</h4>
                    </QueueHeader>
                    { queue.posts.map((post) => {
                      const postShow = post as postView;
                      return (
                        <QueueItem onClick={() => {
                          navigate({
                            pathname: '/browse',
                            search: `?postId=${postShow.post_id}`,
                          });
                        }}>
                          <Heading>{postShow.heading}</Heading>
                          <div></div>
                          <AuthorView userId={postShow.author}></AuthorView>
                          <div></div>
                        </QueueItem>
                      )
                    })}
                  </StyledQueue>
                  <span></span>
                </FlexWrapper>
              )
            })}
            </QueueCols>
          </StyledViewOnlyQueues>
        </StyledLayout>
        
      </Layout>
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