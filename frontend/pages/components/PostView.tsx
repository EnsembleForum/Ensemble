import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, postView } from "../../interfaces";
import CommentView from "./CommentView";
import TextView from "./TextView";
import PostContext from "../postContext";
import { theme } from "../../theme";


// Declaring and typing our props
interface Props { }
const StyledPostListView = styled.div`
  width: 100%;
  height: 100vh;
  background-color: ${theme.colors?.background};
  padding: 20px;
  overflow: hidden;
`
// Exporting our example component
const PostView = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  // This is the data we would be APIfetching on props change
  const [currentPost, setCurrentPost] = React.useState<postView>();
  if (currentPost && currentPost?.post_id === postId) {
    return (
      <StyledPostListView>
        <TextView heading={currentPost.heading} text={currentPost.text} author={currentPost.author} reacts={currentPost.reacts}></TextView>
        {
          currentPost.comments.map((commentId) => {
            return (<CommentView key={commentId} commentId={commentId} />);
          })
        }
      </StyledPostListView >
    )
  } else if (postId > 0) {
    const call: APIcall = {
      method: "GET",
      path: "browse/post_view",
      params: { "post_id": postId.toString() }
    }
    ApiFetch(call)
      .then((data) => {
        const postToShow = data as postView;
        postToShow.post_id = postId;
        const call: APIcall = {
          method: "GET",
          path: "browse/post_view",
          params: { "post_id": postId.toString() }
        }
        setCurrentPost(postToShow);
      });
    return (
      <StyledPostListView>
      </StyledPostListView>
    )
  }
  return (
    <StyledPostListView></StyledPostListView>
  );

};

export default PostView;