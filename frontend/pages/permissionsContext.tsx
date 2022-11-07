import React from "react";
import { userPermission } from "../interfaces";

// set the defaults
const userPermissionsArr : userPermission[] = [];
const PermissionsContext = React.createContext({
  userPermissions: userPermissionsArr,
  setUserPermissions: (active:userPermission[]) => {}
});

export default PermissionsContext;
