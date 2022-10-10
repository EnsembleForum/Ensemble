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

