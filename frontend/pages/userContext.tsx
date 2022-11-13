import React from "react";
import { currentUser } from "../interfaces";

// set the defaults
const defaultUser : currentUser = {
  user_id: 0,
  permissions: []
}
const UserContext = React.createContext({
  currentUser: defaultUser,
  setCurrentUser: (active:currentUser) => {}
});

export default UserContext;
