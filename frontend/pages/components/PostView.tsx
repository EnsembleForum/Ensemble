import styled from "@emotion/styled";
import React, { JSXElementConstructor, useEffect } from "react";
import { Box, IconButton, Text } from "theme-ui";
import { ApiFetch, getCurrentUser, getPermission } from "../../App";
import { APIcall, commentView, postView, replyView } from "../../interfaces";
import TextView from "./TextView";
import { theme } from "../../theme";
import CommentContext from "../commentContext";
import { useSearchParams } from "react-router-dom";


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
  const [comments, setComments] = React.useState<commentView[]>();
  const [currentPost, setCurrentPost] = React.useState<postView>();
  let [searchParams, setSearchParams] = useSearchParams();

  async function getPost() {
    const call: APIcall = {
      method: "GET",
      path: "browse/post_view",
      params: { "post_id": searchParams.get("postId") as string }
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
    if (searchParams.get("postId") !== null && searchParams.get('postId') !== '0') {
      getPost();
    }
  },[commentCount])

  // This is the data we would be APIfetching on props change
  if (currentPost && currentPost?.post_id === parseInt(searchParams.get("postId") as string) && comments) {
    return (
      <CommentContext.Provider value={value}>
       <StyledPostListView>
          <TextView 
            heading={currentPost.heading} 
            text={currentPost.text} 
            author={currentPost.author} 
            reacts={currentPost.me_too} 
            id={parseInt(searchParams.get("postId") as string)} 
            userReacted={currentPost.user_reacted} 
            type="post" private={currentPost.private} 
            anonymous={currentPost.anonymous} 
            closed={currentPost.closed} 
            answered={currentPost.answered} 
            showCloseButton={getPermission(31)} 
            showDeleteButton={currentPost.author === getCurrentUser().user_id  || getPermission(32)} 
          />
          <hr/><h2>Replies</h2>
          {
            comments.map((comment) => {
              return (
                  <>
                  <TextView 
                    key = {comment.comment_id} 
                    text={comment.text} reacts={comment.thanks} 
                    type="comment" id={comment.comment_id} 
                    author={comment.author} 
                    userReacted={comment.user_reacted}
                    accepted={comment.accepted}
                    showAcceptButton={currentPost.author === getCurrentUser().user_id || getPermission(13)}
                  />
                  {comment.replies.map((reply) => {
                    const rep = reply as replyView;
                    return (
                      <TextView 
                        text={rep.text} 
                        reacts={rep.thanks} 
                        type="reply" 
                        author={rep.author} 
                        id={rep.reply_id} 
                        commentId={comment.comment_id} 
                        userReacted={rep.user_reacted}/>
                    )
                  })}
                  </>
              )
            })
          }
          <div style={{height: "80px"}}></div>
        </StyledPostListView>
      </CommentContext.Provider>
    )
  } else if (searchParams.get("postId") && searchParams.get('postId') !== '0') {
    getPost();
    return <StyledPostListView> Loading... </StyledPostListView>
  }
  return (
    <StyledPostListView></StyledPostListView>
  );
};

export default PostView;