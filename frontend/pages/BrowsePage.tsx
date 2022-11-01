import styled from "@emotion/styled";
import React, { createContext, JSXElementConstructor, MouseEvent, ReactElement } from "react";
import CreatePostView from "./components/CreatePostView";
import PostListView from "./components/PostListView";
import PostView from "./components/PostView";
import PostContext from "./postContext";

interface Props {}

const StyledLayout = styled.div`
  display: flex;
  height: 100%;
  flex-direction: horizontal;
`
const BrowsePage = (props: Props) => {
  const [postId, setPostId] = React.useState(0);
  const value = { postId, setPostId};
  return (
    <PostContext.Provider value={value}>
      <StyledLayout>
        <PostListView/>
        <PostView postId = {postId} />
        <CreatePostView/>
      </StyledLayout>
    </PostContext.Provider>
  );
};

export default BrowsePage;