import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { postView } from "../../interfaces";

// Declaring and typing our props
interface Props {
  text: string,
  heading?: string,
  reacts?: {
    thanks: number,
    me_too: number
  }
}

const StyledText = styled.div`
  padding: 10px;
`
// Exporting our example component
const PostView = (props: Props) => {
  let heading = <></>;
  let reacts = <></>;
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
  }
  if (props.reacts) {
    reacts = <div>thanks: {props.reacts.thanks} <br/> me_too: {props.reacts.me_too}</div>;
  }
  return (
    <StyledText>
      {heading}
      <p>{props.text}</p>
      {reacts}
    </StyledText>
  );
};

export default PostView;