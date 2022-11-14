import styled from "@emotion/styled";
import React from "react";
import { useSearchParams } from "react-router-dom";
import { ApiFetch } from "../../App";
import { APIcall, postListItem } from "../../interfaces";
import { theme } from "../../theme";
import AuthorView from "./AuthorView";

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
const ActivePost = styled(Post)`
  filter: brightness(95%);
`
const ClosedPost = styled(Post)`
  background-color:#FF7F7F;
`

const Heading = styled.div`
  font-weight: 700;
`

// Exporting our example component
const PostListView = (props: Props) => {
  const [posts, setPosts] = React.useState<postListItem[]>();
  let [searchParams, setSearchParams] = useSearchParams();
  React.useEffect(()=>{
    const api: APIcall = {
      method: "GET",
      path: "browse/post_list",
      params: {"search_term": ""}
    }
    console.log(api);
    ApiFetch(api)
      .then((data) => {
        const test = data as { posts: postListItem[] };
        setPosts(test.posts);
        if (test.posts.length && (searchParams.get('postId') === null || searchParams.get('postId') === '0')) {
          setSearchParams({postId: test.posts[0].post_id.toString()})
        }
      })
  }, [searchParams])


  if (posts && posts.length > 0) {
    return (
      <StyledLayout>
        {
          posts.map((each) => {
              const styles : any = {}
              if (each.closed) {
                styles.backgroundColor = "#ffa3a3";
              }
              if (each.answered) {
                styles.backgroundColor = "#90EE90";
              }
              if (each.post_id.toString()===searchParams.get("postId")) {
                if (each.closed) {
                  styles.backgroundColor = "#f08d8d";
                } else if (each.answered) {
                  styles.backgroundColor = "#7de37d";
                } else {
                  styles.backgroundColor = theme.colors?.highlight;
                }
              }
              return (
                <Post style={styles}  onClick={() => setSearchParams({postId: each.post_id.toString()})}>
                  <Heading>{each.heading}</Heading>
                  <AuthorView userId={each.author}/>
                  <div>Tags: {each.tags}</div>
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
    </StyledLayout>
  )
};

export default PostListView;