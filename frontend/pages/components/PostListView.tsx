import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { Button, Input } from "theme-ui";
import { ApiFetch, getPermission } from "../../App";
import { APIcall, postListItem, tag } from "../../interfaces";
import { theme } from "../../theme";
import AuthorView from "./AuthorView";
import ReactTooltip from 'react-tooltip';
import { StyledButton, Tag } from "../GlobalProps";

// Declaring and typing our props
interface Props { }
const StyledLayout = styled.div`
  background-color: ${theme.colors?.muted};
  width: 25vw;
  border-right: 1px solid lightgrey; 
  p {
    margin-left: 10px;
  }
  overflow-y: scroll;
  overflow-x: hidden;
`
const Post = styled.div`
  max-width: 100%;
  height: 50px;
  padding: 10px 20px 25px 20px;
  border-bottom: 1px solid lightgrey;
  &:hover {
    background-color: ${theme.colors?.highlight};
    cursor: pointer;
  }
  * {
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
  }
`

const Heading = styled.div`
  font-weight: 700;
`
const Searchbar = styled(Input)`
  background-color: white;
  border-radius: 10px 0 0 10px;
  height: 35px;
`
const ConvertButton = styled(StyledButton)`
  border-radius: 0px 10px 10px 0px;
  border: 1px solid black;
  border-left: 0;
  height: 35px;
  width: 35px;
  padding: 0;
  background: lightgrey;
`

// Exporting our example component
const PostListView = (props: Props) => {
  const [posts, setPosts] = React.useState<postListItem[]>();
  let [searchParams, setSearchParams] = useSearchParams();
  let [searchTerm, setSearchTerm] = React.useState<string>('');
  let [tags, setTags] = React.useState<tag[]>([]);
  React.useEffect(()=>{
    getTags();
    const api: APIcall = {
      method: "GET",
      path: "browse/post/list",
      params: {"search_term": searchTerm}
    }
    ApiFetch(api)
      .then((data) => {
        const test = data as { posts: postListItem[] };
        setPosts(test.posts);
        if (test.posts.length && (searchParams.get('postId') === null || searchParams.get('postId') === '0')) {
          setSearchParams({postId: test.posts[0].post_id.toString()})
        }
      })
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams, searchTerm])
  async function getTags() {
    const tagCall : APIcall = {
      method: "GET",
      path: "tags/tags_list",
    }
    const tags = await ApiFetch(tagCall) as {tags: tag[]};
    setTags(tags.tags);
  }
  const searchBar = 
  <div style={{padding: "10px", display: "flex"}}>
    <Searchbar placeholder="Search" value={searchTerm} onChange={(e)=>{
      setSearchTerm(e.target.value);
    }}></Searchbar>
    <ReactTooltip place="top" type="dark" effect="solid"/>
    <ConvertButton data-tip="Convert post query into question" onClick={() => {
      searchParams.set("searchTerm", searchTerm);
      setSearchParams(searchParams);
    }}>❓</ConvertButton>
  </div>

  if (posts && posts.length > 0) {
    return (
      <StyledLayout>
        {searchBar}
        {
          posts.map((each) => {
              const styles : any = {}
              if (each.answered) {
                styles.backgroundColor = "#90EE90";
              }
              if (each.closed) {
                styles.backgroundColor = "#a2c4fc";
              }
              if (each.reported && getPermission(33)) {
                styles.backgroundColor = "#ffa3a3";
              }
              if (each.deleted) {
                styles.backgroundColor = "#8c8c8c";
              }
              if (each.post_id.toString()===searchParams.get("postId")) {
                if (!(each.answered || each.reported || each.closed || each.deleted)) {
                  styles.backgroundColor = theme.colors?.highlight;
                }
                if (each.answered) {
                  styles.backgroundColor = "#7de37d";
                } 
                if (each.closed) {
                  styles.backgroundColor = "#7dacfa";
                }   
                if (each.reported) {
                  styles.backgroundColor = "#f08d8d";
                } 
                if (each.deleted) {
                  styles.backgroundColor = "#696969";
                }
              }
              return (
                <Post style={styles}  onClick={() => setSearchParams({postId: each.post_id.toString()})}>
                  <Heading>{each.heading}</Heading>
                  <AuthorView userId={each.author}/>
                  <div>{ tags ? each.tags.map((tag) => {
                    return <Tag style={{marginRight: "5px", marginTop: "5px"}}>{tags.find((e) => { return (e.tag_id === tag) }).name}</Tag>
                  }) : <></>}</div>
                </Post>
              );
            }
          ) 
        }
      </StyledLayout>
    );
  }
  return (
    <StyledLayout>
      {searchBar}
    </StyledLayout>
  )
};

export default PostListView;