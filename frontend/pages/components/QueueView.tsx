import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { Box, IconButton, Input, Select, Text } from "theme-ui";
import { APIcall, postView, queueListPosts } from "../../interfaces";
import { theme } from "../../theme";
import { StyledButton } from "../GlobalProps";
import QueueContext, { UpdateContext } from "../queueContext";
import AuthorView from "./AuthorView";
import QueueItemView from "./QueueItemView";
import ReactTooltip from 'react-tooltip';
import { ApiFetch, getPermission } from "../../App";

// Declaring and typing our props
interface Props {
  queue: queueListPosts,
}
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
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
  h4 {
    color: white;
    border-radius: 10px;
    background-color: ${theme.colors?.primary}; 
  }
  span {
    display: flex;
  }
`


const DeleteButton = styled(StyledButton)`
  min-width: 30px;
  min-height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  font-size: inherit;
  background-color: #ff8080;
  margin-left: 5px;
`
const EditButton = styled(DeleteButton)`
  background-color: #1c9127;
`

// Exporting our example component
const QueueView = (props: Props) => {
  const { queue } = props;
  const {update, setUpdate} = React.useContext(UpdateContext);
  const [toggleDelete, setToggleDelete] = React.useState(false);
  const [toggleEdit, setToggleEdit] = React.useState(false);
  const [editedTitle, setEditedTitle] = React.useState<string>(props.queue.queue_name);
  async function deleteQueue() {
    const deleteQueueCall : APIcall = { 
      method: "DELETE",
      path: "taskboard/queue_list/delete",
      params: {queue_id: queue.queue_id.toString()}
    }
    await ApiFetch(deleteQueueCall);
    setUpdate(!update);
  }
  async function editQueue() {
    if (editedTitle !== props.queue.queue_name) {
      const editQueueCall : APIcall = { 
        method: "PUT",
        path: "taskboard/queue_list/edit",
        body: {queue_id: queue.queue_id, new_name: editedTitle}
      }
      await ApiFetch(editQueueCall);
      setUpdate(!update);
    }
    setToggleEdit(false);
  }

  return (
    <FlexWrapper>
    <StyledQueue
    >
      <QueueHeader onMouseEnter={() => {setToggleDelete(true)}}
      onMouseLeave={() => {setToggleDelete(false)}}>
        { toggleEdit ? 
          <>
            <Input value={editedTitle} onChange={(e) => setEditedTitle(e.target.value)}/>
            <span>
              <EditButton onClick={editQueue}>✅</EditButton>
              <DeleteButton onClick={() => {setToggleEdit(false)}}>❌</DeleteButton>
            </span>
          </>
          :
          <>
          <h3>{queue.queue_name}</h3>
          <span>
            <h4>{queue.posts.length}</h4>
            {toggleDelete && !toggleEdit && getPermission(23) ?  <>
              <>
              <ReactTooltip place="top" type="dark" effect="solid"/>
              <EditButton data-tip="Edit queue name" onClick={() => {setToggleEdit(true)}}>✏️</EditButton>
              </>
              <>
              <ReactTooltip place="top" type="dark" effect="solid"/>
              <DeleteButton data-tip="Delete this queue" onClick={deleteQueue}>🗑️</DeleteButton>
              </>
            </> : <></>}
          </span>
        </>
        }
        
      </QueueHeader>
      { queue.posts.map((post) => {
        const postShow = post as postView;
        return (
          <QueueItemView postShow={postShow} queueId={queue.queue_id} viewOnly={queue.view_only}></QueueItemView>
        )
      })}
    </StyledQueue>
    <span></span>
    </FlexWrapper>
  );
};

export default QueueView;