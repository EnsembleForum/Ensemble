import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { postView } from "../../interfaces";
import CommentView from "./CommentView";
import TextView from "./TextView";

// Declaring and typing our props
interface Props {
  postId: number;
}
const StyledPostListView = styled.div`
  width: 100%;
  height: 100%;
  background-color: lightblue;
  padding: 20px;
  overflow: scroll;
`
// Exporting our example component
const PostView = (props: Props) => {
  // This is the data we would be APIfetching on props change
  /*const fakeDefaultValue : postView = {
    post_id: 1,
    heading: "Post1",
    tags: [1, 2],
    reacts: {
      thanks: 1,
      me_too: 1
    },
    comments: [],
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit"
  }*/
  const fakeDefaultValueList: postView[] = [{
    post_id: 0,
    heading: "Post1",
    tags: [1, 2],
    reacts: {
      thanks: 1,
      me_too: 1
    },
    comments: [0, 1, 2],
    text: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit"
  },
  {
    post_id: 1,
    heading: "Post2",
    tags: [1, 2],
    reacts: {
      thanks: 2,
      me_too: 0
    },
    comments: [0],
    text: "YOOOOOOOt"
  }]

  const postToShow = fakeDefaultValueList[props.postId];
  return (
    <StyledPostListView>
      <TextView heading={postToShow.heading} text={postToShow.text} reacts={postToShow.reacts}></TextView>
      {postToShow.comments.map((commentId) => {
        return (<CommentView key={commentId} commentId={commentId} />);
      })}

    </StyledPostListView>
  );
};

export default PostView;