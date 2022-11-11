import styled from "@emotion/styled";
import React, { createContext, JSXElementConstructor, MouseEvent, ReactElement, useEffect } from "react";
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
  height: 100vh;
`


const BrowsePage = (props: Props) => {
  const [postId, setPostId] = React.useState(0);
  const [load, setLoad] = React.useState(false);
  const value = { postId, setPostId };

  React.useEffect(()=>{
    const api: APIcall = {
      method: "GET",
      path: "browse/post_list",
    }
    ApiFetch(api)
      .then((data) => {
        const test = data as { posts: postListItem[] };
        if (test.posts.length) {
          setPostId(test.posts[0].post_id);
        }
      })
  }, [])
  return (
    <PostContext.Provider value={value}>
      <Layout>
        <Navbar page="browse" />
        <StyledLayout>
          <PostListView />
          <PostView />
        </StyledLayout>
        <CreatePostView />
      </Layout>
    </PostContext.Provider>
  );
};

export default BrowsePage;