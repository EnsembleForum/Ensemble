import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, postView } from "../../interfaces";
import CommentView from "./CommentView";
import TextView from "./TextView";
import PostContext from "../postContext";
import { theme } from "../../theme";
import CommentContext from "../commentContext";


// Declaring and typing our props
interface Props { }
const StyledPostListView = styled.div`
  width: 100%;
  height: 100vh;
  background-color: ${theme.colors?.background};
  padding: 20px;
  overflow-y: scroll;
  overflow-x: hidden;
`
// Exporting our example component
const PostView = (props: Props) => {
  const [commentCount, setCommentCount] = React.useState(0);
  const value = { commentCount, setCommentCount};
  const { postId, setPostId } = React.useContext(PostContext);
  // This is the data we would be APIfetching on props change
  const [currentPost, setCurrentPost] = React.useState<postView>();
  if (currentPost && currentPost?.post_id === postId) {
    return (
      <CommentContext.Provider value={value}>
       <StyledPostListView>
          <TextView heading={currentPost.heading} text={currentPost.text} author={currentPost.author} reacts={currentPost.reacts} id={postId} type={"postcomment"}></TextView>
          <hr/>
          <h3>Replies</h3>
          {
            currentPost.comments.map((commentId) => {
              return (<CommentView key={commentId} commentId={commentId} />);
            })
          }
        </StyledPostListView >
      </CommentContext.Provider>
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
        setCurrentPost(postToShow);
      });
    return (
      <CommentContext.Provider value={value}>
        <StyledPostListView>
        </StyledPostListView>
      </CommentContext.Provider>

    )
  }
  return (
    <CommentContext.Provider value={value}>
      <StyledPostListView></StyledPostListView>
    </CommentContext.Provider>
  );

};

export default PostView;