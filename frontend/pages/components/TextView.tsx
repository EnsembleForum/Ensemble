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
  reacts?: {
    thanks: number,
    me_too: number
  },
  type: "postcomment" | "commentreply" | "replyreply",
  answer?: boolean,
}

const StyledText = styled.div`
  padding: 10px;
  border-radius: 2px;
  overflow: hidden;
  * {
    margin-bottom: 10px;
  }
  h1 {
    margin-top: 0px;
  }
`

const StyledPost = styled.div`
  padding-bottom: 10px;
  border-bottom: 1px solid lightgrey;
`


const StyledReply = styled.div`
  display: flex;
  content-align: center;
  button {
    border-radius: 0 10px 10px 0;
    border: 1px solid black;
    border-left: 0;

  }
  input {
    border-right: 0;
    border-radius: 10px 0 0 10px;
  }  
`


// Exporting our example component
const TextView = (props: Props) => {
  const [text, setText] = React.useState<string>();
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  const routes = {
    "postcomment": "browse/post_view/comment",
    "commentreply": "browse/comment_view/reply",
    "replyreply": "browse/reply_view/reply",
  }
  let heading = <></>;
  let reacts = <></>;
  let author = <></>
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
  }
  if (props.reacts) {
    reacts = <div>thanks: {props.reacts.thanks} <br /> me_too: {props.reacts.me_too}</div>;
  }
  if (props.author) {
    author = <AuthorView userId={props.author}/>
  }
  return (
    <StyledText>
      <StyledPost>
        {heading}
        {author}
        <p>{props.text}</p>
        {reacts}
      </StyledPost>
      <StyledReply>
        <Input placeholder="Reply" value={text} onChange={(e)=>setText(e.target.value)} ></Input>
        <StyledButton onClick={(e) => {
            const call : APIcall = {
              method: "POST",
              path: routes[props.type],
              body: {"post_id": props.id, "text": text}
            }
            console.log(call);
            ApiFetch(call).then(()=>{
              setCommentCount(commentCount + 1);
            });
        }}>Post</StyledButton>
      </StyledReply>
    </StyledText>
  );
};

export default TextView;