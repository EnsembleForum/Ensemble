import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, commentView, postView, replyView } from "../../interfaces";
import CommentContext from "../commentContext";
import PostContext from "../postContext";
import TextView from "./TextView";

// Declaring and typing our props
interface Props {
  replyId: number;
  commentId: number;
}
const StyledPostListView=styled.div`
margin-left: 30px;
background-color: lightgreen;
`
// Exporting our example component
const ReplyView = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  const [reply, setReply] = React.useState<commentView>();
  if (reply) {
    return (
      <StyledPostListView>
        <TextView text={reply.text} reacts={reply.thanks} type="reply" id={props.commentId} author={reply.author}></TextView>
        {/*reply.replies.map((replyId) => {
          return (<ReplyView key={replyId} replyId={replyId} />);
        })*/}
      </StyledPostListView>
    ); 
  } else {
    const call : APIcall = {
      method: "GET",
      path: "browse/reply_view",
      params: {"reply_id": props.replyId.toString()}
    }
    ApiFetch(call).then((data)=>{
      const out = data as commentView;
      console.log(out);
      setReply(out);
      setCommentCount(commentCount + 1);
    });
    return <>LOL</>
  }
};

export default ReplyView;