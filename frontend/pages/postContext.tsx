import React from "react";

// set the defaults
const PostContext = React.createContext({
  postId: 0,
  setPostId: (active:number) => {}
});

export default PostContext;
