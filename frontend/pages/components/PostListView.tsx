import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { forEachChild } from "typescript";
import { ApiFetch } from "../../App";
import { APIcall, postListItem } from "../../interfaces";
import PostContext from "../postContext";
import PostListItem from "./PostListItem";

// Declaring and typing our props
interface Props { }
const StyledLayout = styled.div`
  width: 350px;
`
const Post = styled.div`
  max-width: 100%;
  height: 50px;
  padding: 20px;
  border-bottom: 1px solid black;
  &:hover {
    background-color: lightgrey;
    cursor: pointer;
  }
  &:active {
    background-color: darkgrey;
  }
  * {
    overflow: hidden;
    text-overflow: ellipsis;
  }
`

// Exporting our example component
const PostListView = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  const [posts, setPosts] = React.useState<postListItem[]>();
  if (posts) {
    console.log(posts);
    return (
      <StyledLayout>
        {
          posts.map((each) => {
            return (
              <Post onClick={() => {
                console.log("setting id", each.post_id);
                setPostId(each.post_id);
              }}>
                <p>{each.heading} <br /> {each.author}<br />{each.tags}</p>
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
      No post selected
    </StyledLayout>
  )
};

export default PostListView;