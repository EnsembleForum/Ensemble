import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { Box, IconButton, Input, Text } from "theme-ui";
import { postView } from "../../interfaces";
import { StyledButton } from "../GlobalProps";
import AuthorView from "./AuthorView";

// Declaring and typing our props
interface Props {
  text?: string,
  heading?: string,
  author?: number,
  reacts?: {
    thanks: number,
    me_too: number
  },
  answer?: boolean;
}

const StyledText = styled.div`
  padding: 10px;
  border-radius: 2px;
  overflow: hidden;
  * {
    margin-bottom: 10px;
  }
  h1 {
    margin-top: 0px;
  }
`
// Exporting our example component
const TextView = (props: Props) => {
  let heading = <></>;
  let reacts = <></>;
  let author = <></>
  if (props.heading) {
    heading = <h1>{props.heading}</h1>
  }
  if (props.reacts) {
    reacts = <div>thanks: {props.reacts.thanks} <br /> me_too: {props.reacts.me_too}</div>;
  }
  if (props.author) {
    author = <AuthorView userId={props.author}/>
  }
  return (
    <StyledText>
      {heading}
      {author}

      <p>{props.text}</p>
      {reacts}

      <div>
        <Input></Input>
        <StyledButton>Post</StyledButton>
      </div>
    </StyledText>
  );
};

export default TextView;