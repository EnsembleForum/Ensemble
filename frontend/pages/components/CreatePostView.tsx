import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { Input, Select, Textarea } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, createPost, tag } from "../../interfaces";
import { StyledButton, Tag } from "../GlobalProps";

// Declaring and typing our props
interface Props {}
const StyledPost = styled.div`
  padding: 10px 10px 0 10px;
  border: 1px solid grey;
  border-radius: 10px;
  overflow: hidden;
  position: absolute;
  bottom: 20px;
  right: 20px;
  * {
    margin-bottom: 11px;
  }
  textarea {
    height: 100px;
  }
  background-color: white;
  width: 500px;
`
const StyledPostButton = styled(StyledButton)`
  position: absolute;
  bottom: 20px;
  right: 20px;
  filter: drop-shadow(0 0 0.5rem crimson);
  &:hover {
    filter: drop-shadow(0 0 0.5rem crimson);
    filter: brightness(85%);
  }
`
const SpreadButtons = styled.div`
  display: flex;
  justify-content: space-between;
  padding-bottom: 0;
  * {
    margin: 0;
  }
`

const TagCreate = styled.div`
  margin-top: 10px;
  display: flex;
`
const TagCreateSelect = styled(Select)`
  border-radius: 10px 0 0 10px;
  height: 40px;
  width: 410px;
`
const TagCreateButton = styled(StyledButton)`
  text-align: center;
  padding: 10px 10px 10px 10px;
  border: 1px solid black;
  border-left: 0;
  height: 40px;
  width: 100px;
  border-radius: 0px 10px 10px 0px;
`
const Close = styled.span`
  border-left: 1px solid white;
  padding-left: 4px;
  margin-left: 4px;
  &:hover {
    cursor: pointer;
  }
`


// Exporting our example component
const CreatePostView = (props: Props) => {
  let [toggle, setToggle] = React.useState<boolean>(false);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  let [searchParams, setSearchParams] = useSearchParams();
  const def : createPost = {
    heading: '',
    tags: [],
    text: '',
    private: false,
    anonymous: false,
  }
  let [post, setPost] = React.useState<createPost>({
    heading: '',
    tags: [],
    text: '',
    private: false,
    anonymous: false,
  });
  let [tags, setTags] = React.useState<tag[]>();
  let [selectedTags, setSelectedTags] = React.useState<tag[]>([]);
  let [currentTag, setCurrentTag] = React.useState<number>(0);

  async function getTags() {
    const tagCall : APIcall = {
      method: "GET",
      path: "tags/tags_list",
    }
    const tags = await ApiFetch(tagCall) as {tags: tag[]};
    if (tags) {
      setTags(tags.tags);
      setCurrentTag(tags.tags[0].tag_id);
    }
  }

  React.useEffect(() => {
    getTags();
    if (searchParams.get('searchTerm')) {
      setToggle(true);
      setPost(post => ({ ...post, heading: searchParams.get('searchTerm') as string }))
    }
  }, [searchParams.get('searchTerm')])

  if (toggle && tags) {
    return (
      <StyledPost>
        <Input placeholder="Heading" value={post.heading} onChange={(e) => setPost(post => ({ ...post, heading: e.target.value }))}></Input>
        <Textarea placeholder="Text" value={post.text} onChange={(e) => setPost(post => ({ ...post, text: e.target.value }))}></Textarea>
        <TagCreate>
          <TagCreateSelect value={currentTag} onChange={(e) => {setCurrentTag(parseInt(e.target.value))}}>
            { tags.map((tag) => {
              return (<option value={tag.tag_id}>{tag.name}</option>)
            })}
          </TagCreateSelect>
          <TagCreateButton onClick={() => {
            const tag = tags?.find((e) => e.tag_id === currentTag);
            const alreadyThere = selectedTags.find((e) => e.tag_id === currentTag);
            if (tag?.tag_id && !alreadyThere?.tag_id) {
              const newTags = [...selectedTags, {...tag}];
              setSelectedTags(newTags);
              setPost(post => ({ ...post, tags: newTags.map(a => a.tag_id)}));
            }
          }}>Add Tag</TagCreateButton>
        </TagCreate>
        {/* This is where tags are displayed*/}
        <div>
          {selectedTags.map((e) => {
            return (
              <Tag style={{marginRight: "5px", marginBottom: "5px"}}>{e.name}
                <Close onClick={() => {
                  let newTags = [...selectedTags];
                  newTags = newTags.filter(function( obj ) {
                    return obj.tag_id !== e.tag_id;
                  });
                  setSelectedTags(newTags);
                  setPost(post => ({ ...post, tags: selectedTags.map(a => a.tag_id)}));
                }}>X</Close>
              </Tag>
            )
          })}
        </div>
        
        Private:
        <input
          type="checkbox"
          checked={post.private}
          onChange={() => {
            const privateChecked = !post.private;
            setPost(post => ({ ...post, private: privateChecked }));}}
          />
        Anonymous:
        <input
          type="checkbox"
          checked={post.anonymous}
          onChange={() => {
            const anonymousChecked = !post.anonymous;
            setPost(post => ({ ...post, anonymous: anonymousChecked }));}}
          />
        <SpreadButtons>
          <StyledButton onClick={(e) => {
            const api: APIcall = {
              method: "POST",
              path: "browse/post/create",
              body: post
            }
            console.log(api);
            ApiFetch(api).then((data) => {
              const d = data as { post_id: number };
              setSearchParams({postId: d.post_id.toString()})
              setSelectedTags([]);
              setPost(def);
            }
            );
          }}>New Post</StyledButton>
          <StyledButton onClick={(e) => { setToggle(false); }}>X</StyledButton>
        </SpreadButtons>
      </StyledPost>
    )
  } else {
    return (
      <StyledPostButton onClick={(e) => { setToggle(true) }}>New Post</StyledPostButton>
    )
  }
};

export default CreatePostView;