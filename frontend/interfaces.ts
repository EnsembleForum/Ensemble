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
  me_too: number,
  answered: boolean,
  closed: boolean,
  reported: boolean,
  deleted: boolean
}

export interface postView {
  queue: string;
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
  user_reacted:boolean,
  answered?: number,
  closed: boolean,
  deleted: boolean,
  reported: boolean
}

export interface commentView {
  user_reacted: boolean;
  thanks: number,
  comment_id: number,
  text: string, replies: number[] | replyView[], timestamp: number, author: number, accepted: boolean,deleted: boolean
}

export interface replyView {
  user_reacted: boolean;
  reply_id: number, 
  text: string, 
  timestamp: number, 
  thanks: number, 
  author: number, 
  deleted: boolean
}

export interface userView {
  [key: string]: any,
  name_first: string, 
  name_last: string, 
  username: string, 
  email: string, 
  user_id: number,
  permission_group: string, 
  pronouns?: string 
}

export interface userPermissionsDetails extends permissionHolder {
  group_id: number;
}

export interface permissionType {
  permission_id: number, name: string
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
  token: string,
  user_id: number,
  logged_in: boolean,
  permissions: userPermission[]
}

export interface queueList {
  queues: {queue_name: string, queue_id: number, view_only: boolean}[]
}


export interface queueListPosts {
  queue_name: string, queue_id: number, view_only: boolean, posts: any[]
}

export interface permissionGroup extends permissionHolder {
  group_id: number, 
  name: string,
}

export interface permissionHolder {
  permissions: userPermission[]
}