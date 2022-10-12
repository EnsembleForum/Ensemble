import styled from "@emotion/styled";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { exampleTest } from "../interfaces";

// Declaring and typing our props
interface Props {
  someProp: string;
  secondProp: exampleTest;
}

// Writing styled components
const StyledExampleComponent = styled.div`
  width: 100%;
  display: grid;
`;
// Styling themeUI / our custom components
const StyledStyledExampleComponent = styled(StyledExampleComponent)`
  width: 100%;
`;
const StyledExampleBox = styled(Box)`
  width: 100%;
`;


// Exporting our example component
const ExampleComponent = (props: Props) => {
  const { someProp, secondProp } = props;
  // Remembering to type useStates - other types won't work here
  const [loginForm, setloginForm] = React.useState<exampleTest>({
    coolName: '',
  });
  return (
    <StyledExampleComponent>
      <div>WOW!</div>
    </StyledExampleComponent>
  );
};

export default ExampleComponent;