import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { useNavigate } from "react-router-dom";
import { Box, IconButton, Text } from "theme-ui";
import { Prettify } from "../../global_functions";
import { theme } from "../../theme";

// Declaring and typing our props
interface Props {
  page: "taskboard" | "browse" | "admin";
}

export const StyledNavbar = styled.div`
  height: 60px;
  width: 100vw;
  display: flex;
  border-bottom: 1px solid lightgrey;

  align-items: center;
  * {
    padding: 10px;
    margin: 10px;
  }
  a {
    background-color: ${theme.colors?.muted};
    border-radius: 10px;
    min-width: 60px;
    display: flex;
    justify-content: center;
    font-weight: 400;
    &:hover {
      cursor: pointer;
      background-color: ${theme.colors?.highlight};
      filter: brightness(50%);
    }
  }
  h1 {
    font-weight: 300;

  }
  background-color: ${theme.colors?.muted};
`;

// Exporting our example component
const Navbar = (props: Props) => {
  const navigate = useNavigate();
  let pages = [
    "browse",
    "taskboard",
    "admin",
  ];
  return (
    <StyledNavbar as="nav">
      <h1>ENSEMBLE</h1>
      {Object.keys(pages).map((i) => {
        const page = pages[parseInt(i)];
        return (<a key={page} style={(page === props.page) ? { filter: "brightness(85%)" } : { filter: "brightness(100%)" }} onClick={(e) => {
          navigate("/" + page)
        }}>{Prettify(page)}</a>)
      })}
    </StyledNavbar>
  );
};

export default Navbar;