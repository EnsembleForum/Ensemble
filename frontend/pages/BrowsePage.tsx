import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import PostListView from "./components/PostListView";
import PostView from "./components/PostView";

interface Props {}

const StyledLayout = styled.div`
  display: flex;
  height: 100%;
  flex-direction: horizontal;
`

const BrowsePage = (props: Props) => {
  return (
    <StyledLayout>
      <PostListView/>
      <PostView/>
    </StyledLayout>
  );
};

export default BrowsePage;