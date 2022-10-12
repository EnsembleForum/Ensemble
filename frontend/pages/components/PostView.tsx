import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";

// Declaring and typing our props
interface Props {}
const StyledPostListView=styled.div`
  width: 100%;
  height: 100%;
  background-color: blue
`
// Exporting our example component
const PostView = (props: Props) => {
  return (
    <StyledPostListView>
      <div>WOW!</div>
    </StyledPostListView>
  );
};

export default PostView;