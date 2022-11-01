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
interface Props {
  text?: string,
  heading?: string,
  reacts?: {
    thanks: number,
    me_too: number
  }
}
const StyledPost = styled.div`
  padding: 10px;
  border: 1px solid grey;
  border-radius: 10px;
  overflow: hidden;
  position: absolute;
  bottom: 10px;
  right: 10px;
  * {
    margin-bottom: 10px;
  }
  button {
    margin-right: 10px;
  }
  background-color: white;
  width: 500px;
`


// Exporting our example component
const CreatePostView = (props: Props) => {
  let [toggle, setToggle] = React.useState<boolean>(false);
  let [post, setPost] = React.useState<createPost>({
    heading: '', 
    tags: [], 
    text: '',
  });
  const { postId, setPostId } = React.useContext(PostContext);
  if (toggle) {
    return (
      <StyledPost>
        <Input placeholder="Heading" value = {post.heading}  onChange={(e) => setPost(post => ({ ...post, heading: e.target.value }))}></Input>
        <Textarea placeholder="Text" value = {post.text}  onChange={(e) => setPost(post => ({ ...post, text: e.target.value }))}></Textarea>
        <Input placeholder="Tags separated by a space" onChange={(e) => {
          try {
            const tmp = e.target.value.split(' ').map(Number).filter(Number).filter( function( item, index, inputArray ) {
              return inputArray.indexOf(item) === index;
            });
            setPost(post => ({ ...post, tags: [...post.tags, ...tmp] }))
          } catch {
            alert("Please only use numbers separated by spaces")
          }
        }}></Input>

        <StyledButton onClick={(e) => {
          const api: APIcall = {
            method: "POST",
            path: "browse/create",
            body: post
          }
          ApiFetch(api).then((data) => {
            const d = data as {post_id: number};
            setPostId(d.post_id - 1);
          }
          );
        }}>Post</StyledButton>
        <StyledButton onClick={(e) => {
          setToggle(false);
        }}>X</StyledButton>
      </StyledPost>
    )
  } else {
    return (
      <StyledButton onClick={(e) => {
        setToggle(true);
      }}>Post</StyledButton>
    )
  }
};

export default CreatePostView;