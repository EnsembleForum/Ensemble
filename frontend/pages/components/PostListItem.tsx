import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { post, postListItem, postView } from "../../interfaces";
import PostContext from "../postContext";

// Declaring and typing our props
interface Props {
  post: postListItem
}

const Post = styled.div`
  max-width: 100%;
  height: 100px;
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
  p {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;  
  }
`
// Exporting our example component
const PostListItem = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  const fakeText =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit";
  return (
    <Post onClick={() => setPostId(props.post.post_id-1)}>
      <div>{props.post.heading}</div>
      <p>{fakeText}</p>
      
    </Post>
  );
};

export default PostListItem;