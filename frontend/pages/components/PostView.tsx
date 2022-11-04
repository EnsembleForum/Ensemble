import styled from "@emotion/styled";
import React, { JSXElementConstructor, useEffect } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch } from "../../App";
import { APIcall, commentView, postView, replyView } from "../../interfaces";
import CommentView from "./CommentView";
import TextView from "./TextView";
import PostContext from "../postContext";
import { theme } from "../../theme";
import CommentContext from "../commentContext";


// Declaring and typing our props
interface Props { }
const StyledPostListView = styled.div`
  width: 100%;
  height: 90vh;
  background-color: ${theme.colors?.background};
  padding: 20px;
  overflow-y: scroll;
  overflow-x: hidden;
`

// Exporting our example component
const PostView = (props: Props) => {
  const [commentCount, setCommentCount] = React.useState(0);
  const value = { commentCount, setCommentCount};
  const { postId, setPostId } = React.useContext(PostContext);
  const [comments, setComments] = React.useState<commentView[]>();
  const [currentPost, setCurrentPost] = React.useState<postView>();

  useEffect(() => {
    async function getPost() {
      console.log("getting post");
      const call: APIcall = {
        method: "GET",
        path: "browse/post_view",
        params: { "post_id": postId.toString() }
      }
      const postToShow = await ApiFetch(call) as postView;
      setCurrentPost(postToShow);
      let promiseArray = [];
      for (const commentId of postToShow.comments) {
        const call : APIcall = {
          method: "GET",
          path: "browse/comment_view",
          params: {"comment_id": commentId.toString()}
        }
        promiseArray.push(ApiFetch(call));
      }
      let commentArray : commentView[] = await Promise.all(promiseArray) as commentView[];
      for (const comment of commentArray) {
        let replyArray = [];
        for (const replyId of comment.replies) {
          const call : APIcall = {
            method: "GET",
            path: "browse/reply_view",
            params: {"reply_id": replyId.toString()}
          }
          replyArray.push(ApiFetch(call));
        }
        comment.replies = await Promise.all(promiseArray) as replyView[];
      }
      setCurrentPost(postToShow);
      setComments(commentArray);
    }
    if (postId !== 0 && !currentPost && !comments) {
      getPost();
    }
  })
  // This is the data we would be APIfetching on props change
  if (currentPost && currentPost?.post_id === postId && comments) {
    return (
      <CommentContext.Provider value={value}>
       <StyledPostListView>
          <TextView heading={currentPost.heading} text={currentPost.text} author={currentPost.author} reacts={currentPost.me_too} id={postId} type="post"></TextView>
          <hr/><h2>Replies</h2>
          {
            comments.map((comment) => {
              return (
                <StyledPostListView>
                  <TextView text={comment.text} reacts={comment.thanks} type="comment" id={postId} author={comment.author}></TextView>
                  {comment.replies.map((reply) => {
                    const rep = reply as replyView;
                    return (
                      <p>{rep.text}, {rep.thanks}, {rep.author}</p>
                      //<TextView text={rep.text} reacts={rep.thanks} type="reply" author={rep.author} id={0}></TextView>
                    )
                  })}
                </StyledPostListView >
              )
            })
          }
        </StyledPostListView>
      </CommentContext.Provider>
    )
  } else if (postId !== 0) {
    return (
      <StyledPostListView> Loading... </StyledPostListView>
    );
  }
  return (
    <StyledPostListView></StyledPostListView>
  );
};

export default PostView;