import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { commentView, postView, replyView } from "../../interfaces";
import TextView from "./TextView";

// Declaring and typing our props
interface Props {
  replyId: number;
}
const StyledPostListView=styled.div`
margin-left: 30px;
background-color: lightgreen;
`
// Exporting our example component
const ReplyView = (props: Props) => {
  const fakeDefaultComments : replyView[] = [{
    text:"reply1",
    timestamp: 0, 
    reacts: {
      thanks: 2,
      me_too: 1,
    }, author: 0
  },
  {
    text:"reply2",
    timestamp: 0, 
    reacts: {
      thanks: 1,
      me_too: 1,
    }, author: 0
  },
  {
    text:"reply3",
    timestamp: 0, 
    reacts: {
      thanks: 333,
      me_too: 1,
    }, author: 0
  },
]

  const replyToShow = fakeDefaultComments[props.replyId];
  return (
    <StyledPostListView>
      <TextView text={replyToShow.text} reacts={replyToShow.reacts}></TextView>
    </StyledPostListView>
  );
};

export default ReplyView;