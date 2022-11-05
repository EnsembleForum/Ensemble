import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { forEachChild } from "typescript";
import { ApiFetch } from "../../App";
import { APIcall, postListItem } from "../../interfaces";
import { theme } from "../../theme";
import PostContext from "../postContext";
import AuthorView from "./AuthorView";
import PostListItem from "./PostListItem";

// Declaring and typing our props
interface Props { }
const StyledLayout = styled.div`
  background-color: ${theme.colors?.muted};
  width: 350px;
  border-right: 1px solid lightgrey; 
  p {
    margin-left: 10px;
  }
  overflow-y: scroll;
  overflow-x: hidden;
`
const Post = styled.div`
  max-width: 100%;
  height: 50px;
  padding: 10px 20px 25px 20px;

  border-bottom: 1px solid lightgrey;
  &:hover {
    background-color: ${theme.colors?.highlight};
    cursor: pointer;
  }
  * {
    text-overflow: ellipsis;
  }
`
const ActivePost = styled(Post)`
  background-color: ${theme.colors?.highlight};
  filter: brightness(95%);
`

// Exporting our example component
const PostListView = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  const [posts, setPosts] = React.useState<postListItem[]>();
  if (posts && posts.length >= postId) {
    return (
      <StyledLayout>
        {
          posts.map((each) => {
            if (each.post_id === postId) {
              return (
                <ActivePost onClick={() => {
                  setPostId(each.post_id);
                }}>
                  {each.heading} <br /> <AuthorView userId={each.author}/><br />Tags: {each.tags}
                </ActivePost>
              );
            }
            return (
              <Post onClick={() => {
                setPostId(each.post_id);
              }}>
                {each.heading} <br /> <AuthorView userId={each.author}/><br />Tags: {each.tags}
              </Post>
            );
          })}
      </StyledLayout>
    );
  } else if (postId > 0) {
    const api: APIcall = {
      method: "GET",
      path: "browse/post_list",
    }
    ApiFetch(api)
      .then((data) => {
        const test = data as { posts: postListItem[] };
        setPosts(test.posts);
      })
  }
  return (
    <StyledLayout>
    </StyledLayout>
  )
};

export default PostListView;