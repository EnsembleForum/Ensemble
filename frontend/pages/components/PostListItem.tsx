import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { post } from "../../interfaces";

// Declaring and typing our props
interface Props {
  post: post
}
const StyledLayout=styled.div`
  width: 350px;
  height: 100%;
`
const Post = styled.div`
  height: 100px;
`
// Exporting our example component
const PostListItem = (props: Props) => {
  return (
    <StyledLayout>
      <div>WOW!</div>
    </StyledLayout>
  );
};

export default PostListItem;