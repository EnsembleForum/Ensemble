import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Input, Text, Textarea } from "theme-ui";
import { TypeFlags } from "typescript";
import { ApiFetch } from "../../App";
import { APIcall, createPost, postView } from "../../interfaces";
import { StyledButton } from "../GlobalProps";
import PostContext from "../postContext";
import TaskboardPage from "../TaskboardPage";
import TextView from "./TextView";

// Declaring and typing our props
interface Props {}
const StyledPost = styled.div`
  padding: 10px 10px 0 10px;
  border: 1px solid grey;
  border-radius: 10px;
  overflow: hidden;
  position: absolute;
  bottom: 20px;
  right: 20px;
  * {
    margin-bottom: 11px;
  }
  textarea {
    height: 100px;
  }
  background-color: white;
  width: 500px;
`
const StyledPostButton = styled(StyledButton)`
  position: absolute;
  bottom: 20px;
  right: 20px;
  filter: drop-shadow(0 0 0.5rem crimson);
  &:hover {
    filter: drop-shadow(0 0 0.5rem crimson);
    filter: brightness(85%);
  }
`
const SpreadButtons = styled.div`
  display: flex;
  justify-content: space-between;
  padding-bottom: 0;
  * {
    margin: 0;
  }
`


// Exporting our example component
const CreatePostView = (props: Props) => {
  let [toggle, setToggle] = React.useState<boolean>(false);
  let [post, setPost] = React.useState<createPost>({
    heading: '',
    tags: [],
    text: '',
    private: false,
    anonymous: false,
  });
  const { postId, setPostId } = React.useContext(PostContext);
  if (toggle) {
    return (
      <StyledPost>
        <Input placeholder="Heading" value={post.heading} onChange={(e) => setPost(post => ({ ...post, heading: e.target.value }))}></Input>
        <Textarea placeholder="Text" value={post.text} onChange={(e) => setPost(post => ({ ...post, text: e.target.value }))}></Textarea>
        <Input placeholder="Tags separated by a space" onChange={(e) => {
          try {
            const tmp = e.target.value.split(' ').map(Number).filter(Number).filter(function (item, index, inputArray) {
              return inputArray.indexOf(item) === index;
            });
            setPost(post => ({ ...post, tags: [...post.tags, ...tmp] }))
          } catch {
            alert("Please only use numbers separated by spaces")
          }
        }}></Input>
        <SpreadButtons>
          <StyledButton onClick={(e) => {
            const api: APIcall = {
              method: "POST",
              path: "browse/create",
              body: post
            }
            ApiFetch(api).then((data) => {
              const d = data as { post_id: number };
              setPostId(d.post_id);
            }
            );
          }}>New Post</StyledButton>
          <StyledButton onClick={(e) => { setToggle(false); }}>X</StyledButton>
        </SpreadButtons>

      </StyledPost>
    )
  } else {
    return (
      <StyledPostButton onClick={(e) => { setToggle(true) }}>New Post</StyledPostButton>
    )
  }
};

export default CreatePostView;