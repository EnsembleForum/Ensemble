import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Input, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, postView } from "../../interfaces";
import CommentContext from "../commentContext";
import { StyledButton } from "../GlobalProps";
import AuthorView from "./AuthorView";

// Declaring and typing our props
interface Props {
  text: string,
  heading?: string,
  author?: number,
  id: number,
  reacts: number,
  type: "postcomment" | "commentreply" | "replyreply",
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
  padding-bottom: 10px;
`
const StyledBorder = styled.div`
  height: 1px;
  border-bottom: black;
`

const StyledReply = styled.div`
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
  border-radius: 0;
`


// Exporting our example component
const TextView = (props: Props) => {
  const [text, setText] = React.useState<string>();
  const [toggleReply, setToggleReply] = React.useState<boolean>(false);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  const routes = {
    "postcomment": ["browse/post_view/comment", "Me too: "],
    "commentreply": ["browse/comment_view/reply", "Thanks: "],
    "replyreply": ["browse/reply_view/reply", "Thanks: "],
  }
  let heading = <></>;
  let reacts = <></>;
  let author = <></>
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
  }
  if (props.reacts) {
    reacts = <div>{routes[props.type][1]} {props.reacts}</div>;
  }
  if (props.author) {
    author = <AuthorView userId={props.author}/>
  }
  const reply = (
  <StyledReply>
    <Input placeholder="Reply" value={text} onChange={(e)=>setText(e.target.value)} ></Input>
    <StyledPostButton onClick={(e) => {
        const call : APIcall = {
          method: "POST",
          path: routes[props.type][0],
          body: {"post_id": props.id, "text": text}
        }
        console.log(call);
        ApiFetch(call).then(()=>{
          setCommentCount(commentCount + 1);
        });
    }}>Post</StyledPostButton>
    <StyledReplyButton onClick={(e) => setToggleReply(false)}>X</StyledReplyButton>
  </StyledReply>)
  const replyButton = (<StyledButton onClick={(e) => setToggleReply(true)}>Reply</StyledButton>);

  return (
    <StyledText>
      <StyledPost>
        {heading}
        {author}
        <p>{props.text}</p>
        {reacts}
        { toggleReply ? reply : replyButton}
      </StyledPost>
      { props.type === "postcomment" ? <></>: <StyledBorder/>}
    </StyledText>
  );
};

export default TextView;