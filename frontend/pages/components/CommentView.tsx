import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { commentView, postView } from "../../interfaces";
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
  const fakeDefaultComments : commentView[] = [{
    text:"comment1",
    replies: [0, 2], 
    timestamp: 0, 
    reacts: {
      thanks: 2,
      me_too: 1,
    }, author: 0
  },
  {
    text:"comment2",
    replies: [1], 
    timestamp: 0, 
    reacts: {
      thanks: 2,
      me_too: 1,
    }, author: 0
  },
  {
    text:"comment3",
    replies: [1, 2], 
    timestamp: 0, 
    reacts: {
      thanks: 2,
      me_too: 1,
    }, author: 0
  },
]

  const comment = fakeDefaultComments[props.commentId];
  return (
    <StyledPostListView>
      <TextView text={comment.text} reacts={comment.reacts}></TextView>
      {comment.replies.map((reply) => {
        return (<ReplyView key={reply} replyId={reply}/>);
      })}

    </StyledPostListView>
  );
};

export default CommentView;