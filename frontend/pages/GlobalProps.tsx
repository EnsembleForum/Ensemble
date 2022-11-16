import styled from "@emotion/styled";
import { Box, Button } from "theme-ui";
import { theme } from "../theme";

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

export const Tag = styled.span`
  height: 10px;
  font-weight: 700;
  background-color: ${theme.colors?.highlight};
`;