import styled from "@emotion/styled";
import React, { createContext, JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { ApiFetch } from "../App";
import { APIcall, postListItem } from "../interfaces";
import CreatePostView from "./components/CreatePostView";
import Navbar from "./components/Navbar";
import PostListView from "./components/PostListView";
import PostView from "./components/PostView";
import PostContext from "./postContext";

interface Props { }

const StyledLayout = styled.div`
  display: flex;
  height: 100%;
  flex-direction: horizontal;
`

const Layout = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: 100%;
`


const BrowsePage = (props: Props) => {
  const [postId, setPostId] = React.useState(0);
  const [load, setLoad] = React.useState(false);
  console.log(postId);
  const value = { postId, setPostId };
  if (!load) {
    const api: APIcall = {
      method: "GET",
      path: "browse/post_list",
    }
    ApiFetch(api)
      .then((data) => {
        const test = data as { posts: postListItem[] };
        setPostId(test.posts.length);
        setLoad(true);
      })
  }
  return (
    <PostContext.Provider value={value}>
      <Layout>
        <Navbar page="browse" />
        <StyledLayout>
          <PostListView />
          <PostView />
          <CreatePostView />
        </StyledLayout>
      </Layout>
    </PostContext.Provider>
  );
};

export default BrowsePage;