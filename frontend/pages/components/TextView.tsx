import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, IconButton, Input, Text, Textarea } from "theme-ui";
import { isPropertySignature } from "typescript";
import { ApiFetch } from "../../App";
import { APIcall, postView } from "../../interfaces";
import { theme } from "../../theme";
import CommentContext from "../commentContext";
import { StyledButton } from "../GlobalProps";
import AuthorView from "./AuthorView";

// Declaring and typing our props
interface Props {
  text: string,
  private?: boolean,
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
  margin: 0;
`


const Private = styled.div`
  margin-left: 10px;
  background-color: lightgrey;
  margin-right: 20px;
  padding: 5px;
  border-radius: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  text-align: center;
  max-width: 100px;
`


// Exporting our example component
const TextView = (props: Props) => {
  const [inputText, setInputText] = React.useState<string>();
  const [toggleReply, setToggleReply] = React.useState<boolean>(false);
  const [editHeading, setEditHeading] = React.useState<string>(props.heading as string);
  const [editText, setEditText] = React.useState<string>(props.text as string);
  const [toggleEdit, setToggleEdit] = React.useState<boolean>(false);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);

  const routes = {
    "post": ["browse/post_view/comment", "✋ ", "browse/post_view/react", "post_id", "post_id", "browse/post_view/edit"],
    "comment": ["browse/comment_view/reply", "👍 ", "browse/comment_view/react", "comment_id", "comment_id", "browse/comment_view/edit"],
    "reply": ["browse/comment_view/reply", "👍 ", "browse/reply_view/react", "comment_id", "reply_id", "browse/reply_view/edit"],
  }
  let heading = <></>;
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
  }
  let tags = <></>;
  if (props.tags) {
    console.log(tags);
    tags = <>Tags: {props.tags.map((each) => {return <>{each} </>})}</>
  }
  let author = <AuthorView userId={props.author}/>

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
        console.log("ID:", props.id, call);
        ApiFetch(call).then(()=>{
          setCommentCount(commentCount + 1);
          setToggleReply(false);
        });
    }}>Post</ActiveReactButton>
  </StyledReply>)
  const replyButton = (<InactiveReactButton onClick={() => setToggleReply(true)}>↩️</InactiveReactButton>);
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
        console.log(call);
        ApiFetch(call).then(
          () => {
            setToggleEdit(false);
            setCommentCount(commentCount + 1);
          }
        );
      }}>Post</StyledButton>
    </>
  );
  const editButton = (<InactiveReactButton onClick={() => setToggleEdit(true)}>✍️</InactiveReactButton>);
  const activeEditButton = (<ActiveReactButton onClick={() => setToggleEdit(false)}>✍️</ActiveReactButton>);
  return (
    <StyledText>
      <StyledPost style={props.type === "reply" ? {paddingLeft: "20px", borderLeft: "2px solid lightgrey"} : {}}>
        <OptionsBar>
          {heading}
          {props.private ? <Private>PRIVATE</Private>: <></>}
        </OptionsBar>
        {author}
        {toggleEdit ? <></> : tags}
        <br/>
        {toggleEdit ? editBox : <p>{props.text}</p>}
        {props.userReacted ? 
          <ActiveReactButton onClick={() => react()}>{routes[props.type][1]} <>{
            props.reacts }</></ActiveReactButton>
          :
          <InactiveReactButton onClick={() => react()}>{routes[props.type][1]} <>{
            props.reacts }</></InactiveReactButton>
        }
        { toggleReply ? activeReplyButton : replyButton }
        { toggleEdit ? activeEditButton : editButton }
        { toggleReply ? reply : <></>}
      </StyledPost>
      { props.type === "post" ? <></>: <StyledBorder/>}
    </StyledText>
  );
};

export default TextView;