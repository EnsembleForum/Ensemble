import React from "react";

// set the defaults
const CommentContext = React.createContext({
  commentCount: 0,
  setCommentCount: (active:number) => {}
});
export default CommentContext;
