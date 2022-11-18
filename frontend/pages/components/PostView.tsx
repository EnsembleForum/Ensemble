import styled from "@emotion/styled";
import React, { useEffect } from "react";
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
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  let [searchParams, setSearchParams] = useSearchParams();
  const customRef = React.useRef<HTMLHeadingElement>(null);
  function scrollToNotif() {
    if (customRef.current) {
      const offsetBottom = customRef.current.offsetTop + customRef.current.offsetHeight - 225;
      const scrollableDiv = document.getElementById("scroll");
      if (scrollableDiv) {
        scrollableDiv.scrollTo({ top: offsetBottom, behavior: "smooth" });
      }
    }
  }


  async function getPost() {
    const call: APIcall = {
      method: "GET",
      path: "browse/post/view",
      params: { "post_id": searchParams.get("postId") as string }
    }
    const postToShow = await ApiFetch(call) as postView;
    let commentArray : commentView[] = [];
    for (const commentId of postToShow.comments) {
      const call : APIcall = {
        method: "GET",
        path: "browse/comment/view",
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
          path: "browse/reply/view",
          params: {"reply_id": replyId.toString()}
        }
        const reply = await ApiFetch(call) as replyView;
        replyArray.push(reply);
      }
      comment.replies = replyArray;
    }
    setCurrentPost(postToShow);
    setComments(commentArray);
    scrollToNotif();
  }

  useEffect(() => {
    if (searchParams.get("postId") !== null && searchParams.get('postId') !== '0') {
      getPost();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  },[commentCount, searchParams])
  const exclude = [null, '', '0'];

  // This is the data we would be APIfetching on props change
  if (currentPost && currentPost?.post_id === parseInt(searchParams.get("postId") as string) && comments) {
    return (
      <CommentContext.Provider value={value}>
       <StyledPostListView id="scroll">
          <TextView 
            heading={currentPost.heading} 
            text={currentPost.text} 
            author={currentPost.author} 
            reacts={currentPost.me_too} 
            tags={currentPost.tags}
            id={parseInt(searchParams.get("postId") as string)} 
            userReacted={currentPost.user_reacted} 
            type="post" private={currentPost.private} 
            anonymous={currentPost.anonymous} 
            closed={currentPost.closed} 
            answered={currentPost.answered} 
            reported={currentPost.reported} 
            showCloseButton={getPermission(31)} 
            deleted={currentPost.deleted}
            showDeleteButton={currentPost.author === getCurrentUser().user_id  || getPermission(32)} 
            showReportButton={currentPost.author !== getCurrentUser().user_id && getPermission(30) && !getPermission(33)} 
            showUnreportButton={getPermission(33)} 
            queue={currentPost.author === getCurrentUser().user_id || getPermission(20) ? currentPost.queue : ''}
            focus={!exclude.includes(searchParams.get("notificationId")) && !exclude.includes(searchParams.get("postId")) && searchParams.get("postId") === currentPost.post_id.toString() && exclude.includes(searchParams.get("replyId")) && exclude.includes(searchParams.get("commentId"))}
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
                    deleted={comment.deleted}
                    showAcceptButton={currentPost.author === getCurrentUser().user_id || getPermission(13)}
                    showDeleteButton={comment.author === getCurrentUser().user_id  || getPermission(32)}
                    focus={ !exclude.includes(searchParams.get("commentId")) && exclude.includes(searchParams.get("replyId")) && searchParams.get("commentId") === comment.comment_id.toString()}
                    ref={customRef} 
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
                        deleted={rep.deleted}
                        userReacted={rep.user_reacted}
                        showDeleteButton={rep.author === getCurrentUser().user_id  || getPermission(32)} 
                        focus={ !exclude.includes(searchParams.get("replyId")) && searchParams.get("replyId") === rep.reply_id.toString() }
                        ref={customRef} 
                      />
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