import styled from "@emotion/styled";
import { Box, Button } from "theme-ui";

export const StyledButton = styled(Button)`
  cursor: pointer;
  &:hover {
    filter: brightness(85%);
  }
  &:active {
    background-color:  brightness(50%);
  }
`
export const StyledForm = styled(Box)`
  border: 1px solid black;
  padding: 10px;
  border-radius: 2%;
`;