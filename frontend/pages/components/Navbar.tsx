import styled from "@emotion/styled";
import React from "react";
import { useNavigate } from "react-router-dom";
import { ApiFetch, getCurrentUser, getLoggedIn, getPermission, setCurrentUser } from "../../App";
import { Prettify } from "../../global_functions";
import { APIcall, notification, notifications } from "../../interfaces";
import { theme } from "../../theme";
import { StyledButton } from "../GlobalProps";

// Declaring and typing our props
interface Props {
  page: "taskboard" | "browse" | "admin" | "login" | "profile" | "notifications";
}

export const StyledNavbar = styled.div`
  height: 10vh;
  min-height: 10vh;
  width: 100vw;
  display: flex;
  border-bottom: 1px solid lightgrey;
  align-items: center;
  * {
    padding: 10px;
    margin: 10px;
  }
  a {
    background-color: ${theme.colors?.muted};
    border-radius: 10px;
    min-width: 60px;
    display: flex;
    justify-content: center;
    align-content: center;
    font-weight: 400;
    &:hover {
      cursor: pointer;
      background-color: ${theme.colors?.highlight};
      filter: brightness(50%);
    }
  }
  h1 {
    font-weight: 300;
  }
  button {
    margin-right: 10px;
  }
  span {
    flex-grow: 1;
  }
  background-color: ${theme.colors?.muted};
    overflow: hidden;

`;

const NotifsButton = styled(StyledButton)`
  background-color: inherit;
  padding: 3px 10px 3px 10px;
  font-size: 26px;
  margin-left: auto;
`
const ActiveNotifsButton = styled(NotifsButton)`
  background-color: ${theme.colors?.primary};
  padding: 3px 10px 3px 10px;
  font-size: 26px;
`


const StyledNotifList = styled.div`
  position: absolute;
  width: 100px;
  z-index: 100;
  padding: 10px;
  border-top: 1000px;
  border-radius: 10px;
  overflow: hidden;
  padding-top: 10px;
  * {
    margin-bottom: 10px;
  }
  background: ${theme.colors?.highlight};
`
const NotifItem = styled.div`
  width: 320px;
  display: flex;
`
const NumNotifs = styled.span`
  color: white;
  border-radius: 10px;
  padding: 2px;
  margin: 0px;
  margin-left: 10px;
  background-color: ${theme.colors?.primary}; 
`

const ActiveNotif = styled.a`
  background-color: ${theme.colors?.primary}; 
`


// Exporting our example component
const Navbar = (props: Props) => {
  const navigate = useNavigate();
  const [numNotifs, setNumNotifs] = React.useState<number>(0);
  const [update, setUpdate] = React.useState<boolean>(false);

  React.useEffect(()=>{
    console.log("cool beans")
    const api: APIcall = {
      method: "GET",
      path: "notifications/list",
    }
    ApiFetch(api)
      .then((data) => {
        const notifications = data as {notifications: notification[]};
        const newNumNotifs = notifications.notifications.filter(each => { return !each.seen }).length;   
        setNumNotifs(newNumNotifs);
        setTimeout(() => {setUpdate(!update)}, 5000);
      });
  }, [update]);


  const logout = (
  <StyledButton onClick={(e) => {
    const api: APIcall = {
      method: "POST",
      path: "auth/logout",
    }
    // eslint-disable-next-line no-restricted-globals
    ApiFetch(api).then(()=>{
      const currentUser = getCurrentUser();
      currentUser.logged_in = false;
      setCurrentUser(currentUser);
      navigate("/login");
    });
  }}>Logout</StyledButton>);
  const login = (<StyledButton onClick={(e) => {navigate("/login")}}>Login</StyledButton>);
  let pages = [
    "browse"
  ];
  if (getPermission(20)) {
    pages.push("taskboard")
  }
  if (getPermission(40)) {
    pages.push("admin")
  }
  pages.push("profile")
  return (
    <StyledNavbar as="nav">
      <h1>ENSEMBLE</h1>
      {getLoggedIn() ? Object.keys(pages).map((i) => {
        const page = pages[parseInt(i)];
        return (
          // eslint-disable-next-line jsx-a11y/anchor-is-valid
          <a key={page} style={(page === props.page) ? { filter: "brightness(85%)" } : { filter: "brightness(100%)" }} onClick={() => {
            navigate("/" + page);
          }}>{Prettify(page)}</a>) 
      }) : <></>
      }
     { /* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
     { numNotifs ? 
      <ActiveNotif 
        style={("notifications" === props.page) ? { filter: "brightness(85%)" } : { filter: "brightness(100%)" }} 
        onClick={() => { navigate("/notifications")}}
      >
      Notifications: {numNotifs}
      </ActiveNotif> :
      <>
      { /* eslint-disable-next-line jsx-a11y/anchor-is-valid */}
      <a 
        style={("notifications" === props.page) ? { filter: "brightness(85%)" } : { filter: "brightness(100%)" }} 
        onClick={() => { navigate("/notifications")}}
      >Notifications</a>
      </>
     }
      <span></span>
      {getLoggedIn() ? logout : login }
    </StyledNavbar>
  );
};

export default Navbar;