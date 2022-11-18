import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import CreatePostView from "./components/CreatePostView";
import Navbar from "./components/Navbar";
import PostListView from "./components/PostListView";
import PostView from "./components/PostView";

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
  overflow: hidden;
`


const BrowsePage = (props: Props) => {
  let [searchParams, setSearchParams] = useSearchParams();
  return (
    <Layout>
      <Navbar page="browse" />
      <StyledLayout>
        <PostListView />
        <PostView />
      </StyledLayout>
      <CreatePostView />
    </Layout>
  );
};

export default BrowsePage;