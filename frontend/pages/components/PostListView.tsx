import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { useSearchParams } from "react-router-dom";
import { Box, IconButton, Text } from "theme-ui";
import { forEachChild } from "typescript";
import { ApiFetch } from "../../App";
import { APIcall, postListItem } from "../../interfaces";
import { theme } from "../../theme";
import AuthorView from "./AuthorView";

// Declaring and typing our props
interface Props { }
const StyledLayout = styled.div`
  background-color: ${theme.colors?.muted};
  width: 25vw;
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
    overflow: hidden;
    white-space: nowrap;
  }
`
const ActivePost = styled(Post)`
  background-color: ${theme.colors?.highlight};
  filter: brightness(95%);
`

const Heading = styled.div`
  font-weight: 700;
`

// Exporting our example component
const PostListView = (props: Props) => {
  const [posts, setPosts] = React.useState<postListItem[]>();
  let [searchParams, setSearchParams] = useSearchParams();
  React.useEffect(()=>{
    const api: APIcall = {
      method: "GET",
      path: "browse/post_list",
    }
    ApiFetch(api)
      .then((data) => {
        const test = data as { posts: postListItem[] };
        setPosts(test.posts);
      })
  }, [searchParams])


  if (posts && posts.length > 0) {
    return (
      <StyledLayout>
        {
          posts.map((each) => {
            if (each.post_id === parseInt(searchParams.get("postId") as string)) {
              return (
                <ActivePost onClick={() => {
                  setSearchParams({postId: each.post_id.toString()});
                }}>
                  <Heading>{each.heading}</Heading>
                <AuthorView userId={each.author}/>
                <div>Tags: {each.tags}</div>
                </ActivePost>
              );
            }
            return (
              <Post onClick={() => {
                setSearchParams({postId: each.post_id.toString()})
              }}>
                <Heading>{each.heading}</Heading>
                <AuthorView userId={each.author}/>
                <div>Tags: {each.tags}</div>
              </Post>
            );
          })}
      </StyledLayout>
    );
  }
  return (
    <StyledLayout>
    </StyledLayout>
  )
};

export default PostListView;