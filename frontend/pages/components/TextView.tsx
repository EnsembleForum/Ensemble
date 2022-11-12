import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, IconButton, Input, Text, Textarea } from "theme-ui";
import { isPropertySignature, JsxElement } from "typescript";
import { ApiFetch, getPermission } from "../../App";
import { APIcall, postView } from "../../interfaces";
import { theme } from "../../theme";
import CommentContext from "../commentContext";
import { StyledButton } from "../GlobalProps";
import UserContext from "../userContext";
import PermissionsContext from "../userContext";
import AuthorView from "./AuthorView";
import ReactTooltip from 'react-tooltip';

// Declaring and typing our props
interface Props {
  text: string,
  private?: boolean,
  anonymous?: boolean,
  heading?: string,
  author: number,
  id: number,
  commentId?: number,
  reacts: number,
  userReacted: boolean,
  type: "post" | "comment" | "reply",
  tags?: number[],
  answer?: boolean,
}

const StyledText = styled.div`
  border-radius: 2px;
  overflow: hidden;
  * {
    margin-bottom: 10px;
  }
  h1 {
    margin-top: 0px;
  }
  hr {
    color: white;
  }
`
const StyledPost = styled.div`
`
const StyledBorder = styled.div`
  height: 1px;
  border-bottom: black;
`

const StyledReply = styled.div`
  margin-top: 5px;
  display: flex;
  content-align: center;
  button {
    border: 1px solid black;
    height: 40px;
  }
  input {
    border-right: 0;
    border-radius: 10px 0 0 10px;
    height: 40px;
  }  
`
const StyledReplyButton = styled(StyledButton)`
    border-radius: 0 10px 10px 0;
`
const StyledPostButton = styled(StyledButton)`
  border-left: 0;
  border-radius: 0 10px 10px 0;
`
const InactiveReactButton = styled(StyledButton)`
  padding: 5px;
  margin-right: 5px;
  background-color: darkgrey;
  color: white;

`
const ActiveReactButton = styled(InactiveReactButton)`
  background-color: ${theme.colors?.primary};
  font-weight: 900;
`

const OptionsBar = styled.div`
  display: flex;
  justify-content: space-between;
  margin: 0;
`


const Private = styled.div`
  margin-left: 10px;
  background-color: lightgrey;
  padding: 5px;
  border-radius: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  text-align: center;
  max-width: 100px;
  height: 30px;
`
const Anonymous = styled(Private)`
  max-width: 130px;
`

const StyledAnonymous = styled.a`
  text-decoration: underline;
  &:hover {
    cursor: pointer;
    font-weight: 700;
  }
`
const Status = styled.span`
  display:flex
`
// Exporting our example component
const TextView = (props: Props) => {
  const [inputText, setInputText] = React.useState<string>();
  const [toggleReply, setToggleReply] = React.useState<boolean>(false);
  const [editHeading, setEditHeading] = React.useState<string>(props.heading as string);
  const [editText, setEditText] = React.useState<string>(props.text as string);
  const [toggleEdit, setToggleEdit] = React.useState<boolean>(false);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  const { currentUser, setCurrentUser } = React.useContext(UserContext);

  const routes = {
    "post": ["browse/post_view/comment", "✋ ", "browse/post_view/react", "post_id", "post_id", "browse/post_view/edit"],
    "comment": ["browse/comment_view/reply", "👍 ", "browse/comment_view/react", "comment_id", "comment_id", "browse/comment_view/edit"],
    "reply": ["browse/comment_view/reply", "👍 ", "browse/reply_view/react", "comment_id", "reply_id", "browse/reply_view/edit"],
  }
  let heading = <></>;
  let author = <></>;
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
  }
  if (props.author) {
    if (props.anonymous && !getPermission(2, currentUser.permissions)) {
      author = <StyledAnonymous>Anonymous</StyledAnonymous>
    } else {
      author = <AuthorView userId={props.author}/>;
    }
  } 


  let tags = <></>;
  if (props.tags) {
    tags = <>Tags: {props.tags.map((each) => {return <>{each} </>})}</>
  }

  function react() {
    const key = routes[props.type][4];
    const call : APIcall = {
      method: "PUT",
      path: routes[props.type][2],
      body: {key: props.id}
    }
    call.body[key] = props.id;
    ApiFetch(call).then(
      () => {
        setCommentCount(commentCount + 1);
      }
    );
  }
  console.log("user:", currentUser);
  const reply = (
  <StyledReply>
    <Input placeholder="Reply" value={inputText} onChange={(e)=>setInputText(e.target.value)} ></Input>
    <ActiveReactButton onClick={(e) => {
        const call : APIcall = {
          method: "POST",
          path: routes[props.type][0],
          body: {"text": inputText}
        }
        if (props.commentId) {
          call.body[routes[props.type][3]] = props.commentId;
        } else {
          call.body[routes[props.type][3]] = props.id;
        }
        ApiFetch(call).then(()=>{
          setCommentCount(commentCount + 1);
          setToggleReply(false);
        });
    }}>Post</ActiveReactButton>
  </StyledReply>)
  const replyButton = (<><ReactTooltip place="top" type="dark" effect="solid"/><InactiveReactButton data-tip="Reply" onClick={() => setToggleReply(true)}>↩️</InactiveReactButton></>);
  const activeReplyButton = (<ActiveReactButton onClick={() => setToggleReply(false)}>↩️</ActiveReactButton>);
  const editBox = (
    <>
      {props.type === "post" ?
      <>
        Tags Todo
        <Textarea value={editHeading} onChange={(e) => setEditHeading(e.target.value)}></Textarea> 
        {/*<Textarea value={editTags} onChange={(e) => setEditTags(e.target.value)}></Textarea>*/}
      </>: <></>
      }
      <Textarea value={editText} onChange={(e) => setEditText(e.target.value)}></Textarea>
      <StyledButton onClick={() => {
        const call : APIcall = {
          method: "PUT",
          path: routes[props.type][5],
          body: { text: editText, }
        }
        call.body[routes[props.type][4]] = props.id;
        if (props.type === "post") {
          call.body.tags = (props.tags ? props.tags : []);
          call.body.heading = editHeading;
        }
        ApiFetch(call).then(
          () => {
            setToggleEdit(false);
            setCommentCount(commentCount + 1);
          }
        );
      }}>Post</StyledButton>
    </>
  );
  const editButton = (<>
  <ReactTooltip place="top" type="dark" effect="solid"/>
  <InactiveReactButton data-tip="Edit" onClick={() => setToggleEdit(true)}>✏️</InactiveReactButton>
  </>);
  const activeEditButton = (<ActiveReactButton onClick={() => setToggleEdit(false)}>✏️</ActiveReactButton>);
  const reactButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <InactiveReactButton data-tip={props.type === "post" ? "Me too!" : "Thanks!"} onClick={() => react()}>{routes[props.type][1]} <>{
            props.reacts }</></InactiveReactButton>
  </>);
  const activeReactButton = (<>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <ActiveReactButton data-tip="Unreact" onClick={() => react()}>{routes[props.type][1]} <>{
            props.reacts }</></ActiveReactButton>
  </>);
  return (
    <StyledText>
      <StyledPost style={props.type === "reply" ? {paddingLeft: "20px", borderLeft: "2px solid lightgrey"} : {}}>
        <OptionsBar>
          {heading}
          <Status>
          {props.private ? <Private>PRIVATE</Private>: <></>}
          {props.anonymous ? <Anonymous>ANONYMOUS</Anonymous>: <></>}
          </Status>
        </OptionsBar>
        {author}
        {toggleEdit ? <></> : tags}
        <br/>
        {toggleEdit ? editBox : <p>{props.text}</p>}
        { props.userReacted ? activeReactButton : reactButton}
        { currentUser.user_id === props.author ? ( toggleEdit ? activeEditButton : editButton ) : <></> }
        { toggleReply ? activeReplyButton : replyButton }
        { toggleReply ? reply : <></>}
      </StyledPost>
      { props.type === "post" ? <></>: <StyledBorder/>}
    </StyledText>
  );
};

export default TextView;