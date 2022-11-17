import styled from "@emotion/styled";
import { stripBasename } from "@remix-run/router";
import React, { JSXElementConstructor, MouseEvent, ReactElement } from "react";
import { useNavigate } from "react-router-dom";
import { IconButton, Text, Box, Label, Input, Checkbox, Select, Textarea, Flex, Button, } from "theme-ui";
import { ApiFetch } from "../App";
import { Prettify } from "../global_functions";
import { APIcall, loginForm, tag, usersRegister, userToAdd } from "../interfaces";
import { theme } from "../theme";
import { StyledButton } from "./GlobalProps";


interface Props { }

const Layout = styled.div`
  height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const Tag = styled.div`
  padding: 3px;
  height: 16px;
  font-size: 14px;
  color: white;
  border-radius: 5px;
  font-weight: bold;
  background-color: ${theme.colors?.primary};
`

const ManageTagsPage = (props: Props) => {
  const navigate = useNavigate();
  const [tags, setTags] = React.useState<tag[]>();
  async function getTags() {
    const tagCall : APIcall = {
      method: "GET",
      path: "tags/tags_list",
    }
    const tags = await ApiFetch(tagCall) as {tags: tag[]};
    setTags(tags.tags);
  }
  React.useEffect(() => {
    getTags();
  }, []);
  return (
    <Layout>
      
      <Tag>cool beans</Tag>
    </Layout>
  );
  
};

export default ManageTagsPage;