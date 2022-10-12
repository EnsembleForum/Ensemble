import styled from "@emotion/styled";
import React from "react";
import { Box, Label, Input, Select } from "theme-ui";
import { ApiFetch } from "../App";
import { Prettify } from "../global_functions";
import { initSchema, loginForm } from "../interfaces";
import { StyledButton } from "./GlobalProps";


interface Props {}

const Navbar = styled.body`
  height: 30px;
  width: 100%;
  
  display: flex;
  align-items: center;
  justify-content: center;
`;

const InitPage = (props: Props) => {
  return (
    <div>
      <></>
    </div>
  );
};

export default InitPage;