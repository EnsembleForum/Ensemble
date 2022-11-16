import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { useSearchParams } from "react-router-dom";
import { Box, IconButton, Text } from "theme-ui";
import CreatePostView from "./components/CreatePostView";
import Navbar from "./components/Navbar";
import NotificationsListView from "./components/NotificationListView";
import PostListView from "./components/PostListView";
import PostView from "./components/PostView";

// Declaring and typing our props
interface Props {}

const StyledLayout = styled.div`
  display: flex;
  height: 100%;
  flex-direction: horizontal;
`
const Layout = styled.div`
  position: fixed;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
`
// Exporting our example component
const NotificationsPage = (props: Props) => {
  let [searchParams, setSearchParams] = useSearchParams();
  return (
    <Layout>
      <Navbar page="notifications" />
      <StyledLayout>
        <NotificationsListView />
        <PostView />
      </StyledLayout>
      <CreatePostView />
    </Layout>
  );
};

export default NotificationsPage;