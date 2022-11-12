import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { Box, IconButton, Text } from "theme-ui";
import { postView, queueListPosts } from "../../interfaces";
import { theme } from "../../theme";
import AuthorView from "./AuthorView";

// Declaring and typing our props
interface Props {
  queue: queueListPosts,
}

// Writing styled components
const StyledQueue = styled.div`
  padding: 10px;
  border-radius: 10px;
  background-color: lightgrey;
  width: 300px;
  min-width: 300px;
  display: flex;
  flex-direction: column;
  margin-right: 30px;
`;
const QueueHeader = styled.div`
  display: flex;
  justify-content: space-between;
  h3, h4 {
    padding: 6px 10px 6px 10px;
    margin: 0;
  }
  h4 {
    color: white;
    border-radius: 10px;
    background-color: ${theme.colors?.primary};
  }
`
const QueueItem = styled.div`
  padding: 10px;
  margin-top: 10px;
  background-color: white;
  border-radius: 10px;
  &:hover {
    cursor: pointer;
    filter: brightness(90%);
  }
`

// Exporting our example component
const QueueView = (props: Props) => {
  const { queue } = props;
  const navigate = useNavigate();
  return (
    <StyledQueue>
      <QueueHeader>
        <h3>{queue.queue_name}</h3>
        <h4>{queue.posts.length}</h4>
      </QueueHeader>
      { queue.posts.map((post) => {
        const postShow = post as postView;
        return (
          <QueueItem onClick={() => {
            navigate({
              pathname: '/browse',
              search: `?postId=${postShow.post_id}`,
            });
    
          }}>
            {postShow.heading}
            <div></div>
            <AuthorView userId={postShow.author}></AuthorView>
            <div></div>
          </QueueItem>
        )
      })}
    </StyledQueue>
  );
};

export default QueueView;