import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, IconButton, Select, Text } from "theme-ui";
import { ApiFetch, getPermission } from "../../App";
import { APIcall, postView, queueListPosts } from "../../interfaces";
import { theme } from "../../theme";
import { StyledButton } from "../GlobalProps";
import QueueContext, { UpdateContext } from "../queueContext";
import AuthorView from "./AuthorView";

// Declaring and typing our props
interface Props {
  postShow: postView,
  viewOnly: boolean,
  queueId: number,
}
const QueueItem = styled.div`
  padding: 10px;
  margin-top: 10px;
  background-color: white;
  border-radius: 10px;
  height: 40px;
  &:hover {
    cursor: pointer;
    filter: brightness(95%);
  }
`

const Heading = styled.div` 
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
`
const RemoveMargin = styled.span`
  * {
    margin: 0px;
  }
`

// Exporting our example component
const QueueItemView = (props: Props) => {
  const navigate = useNavigate();
  const [toggleList, setToggleList] = React.useState(false);
  const {queueList, setQueueList} = React.useContext(QueueContext);
  const {update, setUpdate} = React.useContext(UpdateContext);
  const [selected, setSelected] = React.useState(props.queueId);

  async function setQueue (e: React.ChangeEvent<HTMLSelectElement>) {
    const queueId = parseInt(e.target.value);
    const setQueueCall : APIcall = { 
      method: "PUT",
      path: "taskboard/queue/post_add",
      body: {queue_id: queueId, post_id: props.postShow.post_id}
    }
    await ApiFetch(setQueueCall);
    setUpdate(!update);
  }
  const buttonWidth = props.viewOnly || !getPermission(21) ?  "100%": '';
  return (
    <QueueItem 
    onMouseEnter={() => setToggleList(true)}
    onMouseLeave={() => setToggleList(false)}>
      { toggleList ?
        <span style={{display: "flex", justifyContent: "space-evenly", alignItems: "center"}}> 
          {
            props.viewOnly || !getPermission(21) ? <></> :
            <select style={{width: "80%", padding: "8px", marginRight: "5px", fontSize: "inherit"}} 
              name="permission" id="permission"
              value={selected}
              onChange = {(e) => setQueue(e)}
            >
              {queueList.filter(queue => !queue.view_only).map((queue) => {
                return (<option key={queue.queue_id} value={queue.queue_id} >{queue.queue_name}</option>)
              })}
            </select> 
          }
        <StyledButton style={{height: '40px', paddingTop: "0", paddingBottom: "0", width: buttonWidth}} onClick={() => navigate({
          pathname: '/browse',
          search: `?postId=${props.postShow.post_id}`,
        })}>View</StyledButton>
        </span>
      : 
        <>
          <Heading>{props.postShow.heading}</Heading>
          <div></div>
          <AuthorView userId={props.postShow.author}></AuthorView>
          <div></div>
        </>
      }      
      <div></div>
    </QueueItem>
  )
};

export default QueueItemView;