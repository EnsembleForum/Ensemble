import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, commentView, postView } from "../../interfaces";
import CommentContext from "../commentContext";
import PostContext from "../postContext";
import ReplyView from "./ReplyView";
import TextView from "./TextView";

// Declaring and typing our props
interface Props {
  commentId: number;
}
const StyledPostListView=styled.div`
background-color: lightyellow;

`
// Exporting our example component
const CommentView = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  const { commentCount, setCommentCount } = React.useContext(CommentContext);
  const [comment, setComment] = React.useState<commentView>();
  if (comment) {
    return (
      <StyledPostListView>
        <TextView text={comment.text} reacts={comment.reacts} type="postcomment" id={postId}></TextView>
        {comment.replies.map((replyId) => {
          return (<ReplyView key={replyId} replyId={replyId}/>);
        })}
      </StyledPostListView>
    ); 
  } else {
    const call : APIcall = {
      method: "GET",
      path: "browse/comment_view",
      params: {"comment_id": props.commentId.toString()}
    }
    ApiFetch(call).then((data)=>{
      const out = data as commentView;
      console.log(out);
      setComment(out);
      setCommentCount(commentCount + 1);
    });
    return <>LOL</>
  }
  
};

export default CommentView;