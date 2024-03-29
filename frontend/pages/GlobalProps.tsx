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

export const Tag = styled.div`
  padding: 3px;
  height: 16px;
  font-size: 14px;
  color: white;
  border-radius: 5px;
  font-weight: bold;
  display: inline-block;
  background-color: ${theme.colors?.primary};
`