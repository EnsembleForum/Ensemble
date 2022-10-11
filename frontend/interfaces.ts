import { isStringLiteral } from "typescript"

// Example type
export interface exampleTest {
  coolName: string;
}

// Login form types
export interface loginForm {
  username: string,
  password: string,
}

// Request header type
type HeaderType = "Authorization" | "Content-Type";
export interface requestOptions {
  method: string,
  headers: {
    [header in HeaderType]?: string
  },
  body? : string,
}

// init type
export interface initSchema {
  address: string,
  request_type: "post" | "get",
  username_param: string,
  password_param: string,
  success_regex: string,
  username: string,
  password: string,
  email: string, 
  name_first: string,
  name_last: string
}
