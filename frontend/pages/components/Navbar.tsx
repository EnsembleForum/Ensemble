import styled from "@emotion/styled";
import React, { JSXElementConstructor } from "react";
import { useNavigate } from "react-router-dom";

import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { Prettify } from "../../global_functions";
import { APIcall } from "../../interfaces";
import { theme } from "../../theme";
import { StyledButton } from "../GlobalProps";

// Declaring and typing our props
interface Props {
  page: "taskboard" | "browse" | "admin" | "login";
}

export const StyledNavbar = styled.div`
  height: 10vh;
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
  button {
    margin-right: 10px;
  }
  background-color: ${theme.colors?.muted};
`;

// Exporting our example component
const Navbar = (props: Props) => {
  const navigate = useNavigate();
  const logout = (
  <StyledButton onClick={(e) => {
    const api: APIcall = {
      method: "POST",
      path: "auth/logout",
    }
    // eslint-disable-next-line no-restricted-globals
    ApiFetch(api).then(()=>{
      navigate(0);
    });
  }}>Logout</StyledButton>);
  const login = (<StyledButton onClick={(e) => navigate("/login")}>Login</StyledButton>);

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
      {login} {logout}
    </StyledNavbar>
  );
};

export default Navbar;