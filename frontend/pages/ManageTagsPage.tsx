import styled from "@emotion/styled";
import React from "react";
import { useNavigate } from "react-router-dom";
import { Input } from "theme-ui";
import { ApiFetch } from "../App";
import { APIcall, tag } from "../interfaces";
import { theme } from "../theme";
import { StyledButton } from "./GlobalProps";


interface Props { }

const Layout = styled.div`
  height: 70vh;
  display: flex;
  flex-direction: column;
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
  display: inline-block;
  background-color: ${theme.colors?.primary};
`
const Close = styled.span`
  border-left: 1px solid white;
  padding-left: 4px;
  margin-left: 4px;
  &:hover {
    cursor: pointer;
  }
`
const TagBox = styled.div`
  width: 40vw;
  height: 40vh;
  overflow: auto;
  border: 3px solid lightgrey;
  border-radius: 10px;
  padding: 10px;
  * {
    margin-right: 5px;
    margin-bottom: 5px;
  }
  margin-bottom: 5px;
`
const TagCreate = styled.div`
  display: flex;
`
const TagCreateInput = styled(Input)`
  border-radius: 10px 0 0 10px;
`
const TagCreateButton = styled(StyledButton)`
  padding: 10px 24px 10px 10px;
  border: 1px solid black;
  border-left: 0;
  border-radius: 0px 10px 10px 0px;
`

const ManageTagsPage = (props: Props) => {
  const navigate = useNavigate();
  const [newTag, setNewTag] = React.useState<string>();
  const [tags, setTags] = React.useState<tag[]>();
  const [update, setUpdate] = React.useState<boolean>(false);
  async function getTags() {
    const tagCall : APIcall = {
      method: "GET",
      path: "tags/tags_list",
    }
    const tags = await ApiFetch(tagCall) as {tags: tag[]};
    setTags(tags.tags);
  }
  async function createTag() {
    const tagCall : APIcall = {
      method: "POST",
      path: "tags/new_tag",
      body: {tag_name: newTag}
    }
    await ApiFetch(tagCall);
    setUpdate(!update);
  }
  async function deleteTag(tag_id: number) {
    const tagCall : APIcall = {
      method: "DELETE",
      path: "tags/delete_tag",
      params: {tag_id: tag_id.toString()}
    }
    await ApiFetch(tagCall);
    setUpdate(!update);
  }

  React.useEffect(() => {
    getTags();
  }, [update]);
  return (
    <Layout>
      <TagBox>
        {tags?.map((tag) => {
          return (
            <Tag>{tag.name}<Close onClick={()=>{deleteTag(tag.tag_id)}}>X</Close></Tag>
          )
        })}
      </TagBox>
      <TagCreate>
        <TagCreateInput value={newTag} onChange={(e) => {setNewTag(e.target.value)}} placeholder="New Tag"></TagCreateInput>
        <TagCreateButton onClick={createTag}>Create</TagCreateButton>
      </TagCreate>
    </Layout>
  );
  
};

export default ManageTagsPage;