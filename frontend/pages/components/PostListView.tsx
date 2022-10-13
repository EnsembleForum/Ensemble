import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { post } from "../../interfaces";
import PostListItem from "./PostListItem";

// Declaring and typing our props
interface Props {}
const StyledLayout=styled.div`
  width: 350px;
  height: 100%;
`
const Post = styled.div`
  height: 100px;
`
// Exporting our example component
const PostListView = (props: Props) => {
  const defaultProps : post[] = [{
    post_id: 1,
    heading: "Post1",
    tags: [1, 2],
    reacts: {
      thanks: 1,
      me_too: 1
    }
  }, 
  {
    post_id: 2,
    heading: "Post2",
    tags: [2],
    reacts: {
      thanks: 1,
      me_too: 1
    }
  }];
  return (
    <StyledLayout>
      {defaultProps.map((each) => {
        return <PostListItem post: {each} ></PostListItem>
      })}
      
    </StyledLayout>
  );
};

export default PostListView;