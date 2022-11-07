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

  async function getPost() {
    const call: APIcall = {
      method: "GET",
      path: "browse/post_view",
      params: { "post_id": postId.toString() }
    }
    const postToShow = await ApiFetch(call) as postView;
    let commentArray : commentView[] = [];
    for (const commentId of postToShow.comments) {
      const call : APIcall = {
        method: "GET",
        path: "browse/comment_view",
        params: {"comment_id": commentId.toString()}
      }
      const comment = await(ApiFetch(call)) as commentView;
      commentArray.push(comment);
    }
    console.log("Fetched comments", commentArray);
    for (const comment of commentArray) {
      let replyArray : replyView[] = [];
      for (const replyId of comment.replies) {
        const call : APIcall = {
          method: "GET",
          path: "browse/reply_view",
          params: {"reply_id": replyId.toString()}
        }
        const reply = await ApiFetch(call) as replyView;
        replyArray.push(reply);
      }
      comment.replies = replyArray;
    }
    setCurrentPost(postToShow);
    setComments(commentArray);
  }

  useEffect(() => {
    if (postId !== 0) {
      getPost();
    }
  },[commentCount])

  // This is the data we would be APIfetching on props change
  if (currentPost && currentPost?.post_id === postId && comments) {
    return (
      <CommentContext.Provider value={value}>
       <StyledPostListView>
          <TextView heading={currentPost.heading} text={currentPost.text} author={currentPost.author} reacts={currentPost.me_too} id={postId} userReacted={currentPost.user_reacted} tags={currentPost.tags} type="post"  private={currentPost.private}></TextView>
          <hr/><h2>Replies</h2>
          {
            comments.map((comment) => {
              return (
                  <>
                  <TextView key = {comment.comment_id} text={comment.text} reacts={comment.thanks} type="comment" id={comment.comment_id} author={comment.author} userReacted={comment.user_reacted}></TextView>
                  {comment.replies.map((reply) => {
                    const rep = reply as replyView;
                    return (
                      <TextView text={rep.text} reacts={rep.thanks} type="reply" author={rep.author} id={rep.reply_id} commentId={comment.comment_id} userReacted={rep.user_reacted}></TextView>
                    )
                  })}
                  </>
              )
            })
          }
        </StyledPostListView>
      </CommentContext.Provider>
    )
  } else if (postId !== 0) {
    getPost();
  }
  return (
    <StyledPostListView></StyledPostListView>
  );
};

export default PostView;