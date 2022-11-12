// Example type
export interface exampleTest {
  coolName: string;
}

export interface APIcall {
  [key: string]: any,
  params?: Record<string, string> | undefined;
  method: string, path: string, body?: any, customUrl?: string
}

export interface userToAdd {
  [key: string]: string,
  name_first: string, name_last: string, email: string, username: string,
}
export interface usersRegister {
  users: userToAdd[],
  group_id: number;
}

export interface initReturn {
  user_id: number, token: string, permissions: userPermission[];
}
// you would think you would be able to write data instanceof initReturn 
// but no :((( you have to check individual properties e.g.
function instanceOfInitReturn(object: any): object is initReturn {
  return ('token' in object && 'userId' in object)
}


// Login form types
export interface loginForm {
  username: string,
  password: string,
}

// Request header type
type HeaderType = "Authorization" | "Content-Type" | "Access-Control-Allow-Origin";
export interface requestOptions {
  method: string,
  headers: {
    //[header in HeaderType]?: string
    [key: string]: string;
  },
  body?: string,
}

// init type
export interface initSchema {
  [key: string]: string,
  address: string,
  request_type: string,
  username_param: string,
  password_param: string,
  success_regex: string,
  username: string,
  password: string,
  email: string,
  name_first: string,
  name_last: string
}
export interface reacts {
  thanks: number,
  me_too: number
}
export interface postListItem {
  post_id: number,
  heading: string,
  tags: number[],
  author: number,
  reacts: reacts
}

export interface postView {
  post_id: number,
  author: number,
  heading: string,
  tags: number[],
  me_too: number,
  comments: number[],
  text: string,
  timestamp: number,
  anonymous:boolean,
  private:boolean, 
  user_reacted:boolean
}

export interface commentView {
  user_reacted: boolean;
  thanks: number,
  comment_id: number,
  text: string, replies: number[] | replyView[], timestamp: number, author: number
}

export interface replyView {
  user_reacted: boolean;
  reply_id: number, text: string, timestamp: number, thanks: number, author: number
}

export interface userView {
  name_first: string, name_last: string, username: string, email: string, user_id: number
}

export interface pageList {
  [key: string]: JSX.Element,
}

export interface createPost {
  heading: string,
  tags: number[],
  text: string,
  private:boolean, 
  anonymous:boolean,
}

export interface userPermission {
  permission_id: number,
  value: boolean
}

export interface currentUser {
  user_id: number,
  permissions: userPermission[]
}

export interface queueList {
  queues: {queue_name: string, queue_id: number, view_only: boolean}[]
}


export interface queueListPosts {
  queue_name: string, queue_id: number, view_only: boolean, posts: number[] | postView[]
}