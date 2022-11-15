import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { Input, Textarea } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, createPost } from "../../interfaces";
import { StyledButton } from "../GlobalProps";

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
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  let [searchParams, setSearchParams] = useSearchParams();
  let [post, setPost] = React.useState<createPost>({
    heading: '',
    tags: [],
    text: '',
    private: false,
    anonymous: false,
  });
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
        Private:
        <input
          type="checkbox"
          checked={post.private}
          onChange={() => {
            const privateChecked = !post.private;
            setPost(post => ({ ...post, private: privateChecked }));}}
          />
        Anonymous:
        <input
          type="checkbox"
          checked={post.anonymous}
          onChange={() => {
            const anonymousChecked = !post.anonymous;
            setPost(post => ({ ...post, anonymous: anonymousChecked }));}}
          />
        <SpreadButtons>
          <StyledButton onClick={(e) => {
            const api: APIcall = {
              method: "POST",
              path: "browse/create",
              body: post
            }
            ApiFetch(api).then((data) => {
              const d = data as { post_id: number };
              setSearchParams({postId: d.post_id.toString()})
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