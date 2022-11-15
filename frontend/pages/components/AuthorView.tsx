import styled from "@emotion/styled";
import React, { } from "react";
import { ApiFetch } from "../../App";
import { APIcall, userView } from "../../interfaces";
import { theme } from "../../theme";

// Declaring and typing our props
interface Props {
  userId: number,
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
// Exporting our example component
const AuthorView = (props: Props) => {
  let [toggle, setToggle] = React.useState<boolean>(false);
  const [author, setAuthor] = React.useState<userView>();
  React.useEffect(() => {
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
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])
  if (author) {
    if (toggle) {
      return (
        <span onMouseLeave={(e) => setToggle(false)}>
          <ActiveAuthor>{author.username} </ActiveAuthor>
          <StyledText >
          Email: {author.email} <br/>
          Username: {author.username} <br/>
          Name: {author.name_first} {author.name_last}<br/>
          </StyledText>
        </span>
      )
    } else {
      return (<StyledAuthor onMouseEnter={(e) => setToggle(true)}> {author.username} </StyledAuthor>)
    } 
  }
  return (
    <></>
  );
};

export default AuthorView;