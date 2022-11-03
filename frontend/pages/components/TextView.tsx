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
  const [toggleReact, setToggleReact] = React.useState<number>(0);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  const routes = {
    "postcomment": ["browse/post_view/comment", "Me too: ", "browse/post_view/react", "post_id"],
    "commentreply": ["browse/comment_view/reply", "Thanks: ", "browse/comment_view/react", "comment_id"],
    "replyreply": ["browse/reply_view/reply", "Thanks: ", "browse/reply_view/react", "reply_id"],
  }
  let heading = <></>;
  let reacts = <></>;
  let author = <></>
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
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
        <br/>
        <p>{props.text}</p>
        <StyledButton onClick={(e) => {
          const call : APIcall = {
            method: "PUT",
            path: routes[props.type][2],
            body: {post_id: props.id}
          }
          ApiFetch(call).then(
            () => {
              if (toggleReact) {setToggleReact(0)}
              else {setToggleReact(1)}
            }
          );
        }}>{routes[props.type][1]} {
        toggleReact ? props.reacts + toggleReact : props.reacts - toggleReact}</StyledButton>
        { toggleReply ? reply : replyButton}
      </StyledPost>
      { props.type === "postcomment" ? <></>: <StyledBorder/>}
    </StyledText>
  );
};

export default TextView;