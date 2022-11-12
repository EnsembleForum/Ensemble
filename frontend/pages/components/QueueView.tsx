import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { postView, queueListPosts } from "../../interfaces";
import { theme } from "../../theme";

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
  display: flex;
  flex-direction: column;
`;
const QueueHeader = styled.div`
  display: flex;
  justify-content: space-between;
  h3, h4 {
    padding: 10px;
    margin: 0;
  }
  h4 {
    color: white;
    border-radius: 10px;
    background-color: ${theme.colors?.primary};
  }
  margin-bottom: 10px;
`
const QueueItem = styled.div`
  padding: 10px;
  border-bottom: 10px;
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
  return (
    <StyledQueue>
      <QueueHeader>
        <h3>{queue.queue_name}</h3>
        <h4>{queue.posts.length}</h4>
      </QueueHeader>
      { queue.posts.map((post) => {
        const postShow = post as postView;
        return (
          <QueueItem>
            {postShow.heading}
            {postShow.tags}
          </QueueItem>
        )
      })}
    </StyledQueue>
  );
};

export default QueueView;