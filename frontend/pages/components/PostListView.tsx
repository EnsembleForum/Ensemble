import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { forEachChild } from "typescript";
import { ApiFetch } from "../../App";
import { APIcall, postListItem } from "../../interfaces";
import PostContext from "../postContext";
import PostListItem from "./PostListItem";

// Declaring and typing our props
interface Props {}
const StyledLayout=styled.div`
  width: 350px;
`
// Exporting our example component
const PostListView = (props: Props) => {
  const { postId, setPostId } = React.useContext(PostContext);
  let defaultProps : postListItem[] = [];
  const api: APIcall = {
    method: "GET",
    path: "browse/post_list",
  }
  ApiFetch(api)
    .then((data) => {
      console.log("POSTLISTVUEW:", data);
      defaultProps = data as postListItem[];
    })
  return (
    <StyledLayout>
      {defaultProps.map((each) => {
        console.log("EACH",each);
        return (<PostListItem post={each}></PostListItem>);
      })}
    </StyledLayout>
  );
};

export default PostListView;