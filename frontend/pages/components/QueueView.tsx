import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { Box, IconButton, Select, Text } from "theme-ui";
import { postView, queueListPosts } from "../../interfaces";
import { theme } from "../../theme";
import QueueContext from "../queueContext";
import AuthorView from "./AuthorView";
import QueueItemView from "./QueueItemView";

// Declaring and typing our props
interface Props {
  queue: queueListPosts,
}
const FlexWrapper = styled.div`
  display: flex;
  flex-direction: column;
  content-align: space-between
`
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
console.log("sebfiuesbiu");
// Exporting our example component
const QueueView = (props: Props) => {
  const { queue } = props;
  return (
    <FlexWrapper>
    <StyledQueue>
      <QueueHeader>
        <h3>{queue.queue_name}</h3>
        <h4>{queue.posts.length}</h4>
      </QueueHeader>
      { queue.posts.map((post) => {
        const postShow = post as postView;
        return (
          <QueueItemView postShow={postShow} queueId={queue.queue_id}></QueueItemView>
        )
      })}
    </StyledQueue>
    <span></span>
    </FlexWrapper>
  );
};

export default QueueView;