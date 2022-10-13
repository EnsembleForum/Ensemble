import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { forEachChild } from "typescript";
import { ApiFetch } from "../../App";
import { postListItem } from "../../interfaces";
import PostListItem from "./PostListItem";

// Declaring and typing our props
interface Props {}
const StyledLayout=styled.div`
  width: 350px;
`
// Exporting our example component
const PostListView = (props: Props) => {
  const defaultProps : postListItem[] = [{
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
  const fakeText =  "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit";
  return (
    <StyledLayout>
      {defaultProps.map((each) => {
        return (<PostListItem post={each}></PostListItem>);
      })}
      
    </StyledLayout>
  );
};

export default PostListView;