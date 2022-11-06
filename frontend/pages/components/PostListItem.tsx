import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { postListItem, postView } from "../../interfaces";
import PostContext from "../postContext";

// Declaring and typing our props
interface Props {
  post: postListItem
}

const Post = styled.div`
  max-width: 100%;
  height: 50px;
  padding: 20px;
  &:hover {
    background-color: lightgrey;
    cursor: pointer;
  }
  &:active {
    background-color: darkgrey;
  }
  * {
    overflow: hidden;
    text-overflow: ellipsis;
  }
`
// Exporting our example component
const PostListItem = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  return (
    <Post onClick={() => setPostId(props.post.post_id-1)}>
      <h1>{props.post.heading}</h1>
    </Post>
  );
};

export default PostListItem;