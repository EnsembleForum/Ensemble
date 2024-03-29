import styled from "@emotion/styled";
import React, { } from "react";
import { ApiFetch } from "../../App";
import { APIcall, userView } from "../../interfaces";
import { theme } from "../../theme";

// Declaring and typing our props
interface Props {
  userId: number | null,
}

const StyledAuthor = styled.a`
  text-decoration: underline;
  &:hover {
    cursor: pointer;
    font-weight: 700;
  }
`
const ActiveAuthor = styled(StyledAuthor)`
  margin-top: 0;
`

const StyledText = styled.div`
  position: absolute;
  z-index: 100;
  padding: 10px;
  border-radius: 10px;
  overflow: hidden;
  padding-top: 10px;
  * {
    margin-bottom: 10px;
  }
  background: ${theme.colors?.highlight};
`
const StyledAnonymous = styled.a`
  text-decoration: underline;
  &:hover {
    cursor: pointer;
    font-weight: 700;
  }
`

// Exporting our example component
const AuthorView = (props: Props) => {
  let [toggle, setToggle] = React.useState<boolean>(false);
  const [author, setAuthor] = React.useState<userView>();
  React.useEffect(() => {
    if (props.userId) {
      const call: APIcall = {
        method: "GET",
        path: "user/profile",
        params: { "user_id": props.userId.toString() }
      }
      ApiFetch(call)
        .then((data) => {
          const user = data as userView;
          setAuthor(user);
        });
    }
  }, [])
  if (author) {
    if (toggle) {
      return (
        <span onMouseLeave={(e) => setToggle(false)}>
          <ActiveAuthor>{author.name_first} {author.name_last} {author.permission_group !== "User" ? <>{"[" + author.permission_group + "]"}</>:<></>} </ActiveAuthor>
          <StyledText >
          Name: {author.name_first} {author.name_last}<br/>
          Username: {author.username} <br/>
          Email: {author.email} <br/>
          {author.pronouns ? <>Pronouns: {author.pronouns} <br/></> : <></>}
          </StyledText>
        </span>
      )
    } else {
      return (<StyledAuthor onMouseEnter={(e) => setToggle(true)}> {author.name_first} {author.name_last} {author.permission_group !== "User" ? <>{"[" + author.permission_group + "]"}</>:<></>} </StyledAuthor>)
    }
  }

  if (props.userId === null) {
    return <StyledAnonymous>Anonymous</StyledAnonymous>
  }

  return (
    <></>
  );
};

export default AuthorView;
