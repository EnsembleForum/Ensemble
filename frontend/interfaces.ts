// Example type
export interface exampleTest {
  coolName: string;
}

export interface APIcall {
  method: string, path: string, body?: object | null, customUrl?: string
}

export interface userToAdd {
  [key: string]: string,
  name_first: string, name_last: string, email: string, username: string,
}
export interface usersRegister {
  users: userToAdd[];
}

export interface initReturn {
  [key: string]: any,
  userId: number, token: string
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
  reacts: reacts
}

export interface postView {
  post_id: number,
  heading: string,
  tags: number[],
  reacts: reacts,
  comments: number[],
  text: string,
}
export interface commentView {
  text: string, replies: number[], timestamp: number, reacts: reacts, author: number
}

export interface replyView {
  text: string, timestamp: number, reacts: reacts, author: number
}

export interface userView {
  name_first: string, name_last: string, username: string, email: string, user_id: number
}