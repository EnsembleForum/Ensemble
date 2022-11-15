import { useEffect, useState } from "react";
import { Flex, Heading, Text } from "theme-ui";
import { ApiFetch, getCurrentUser } from "../App";
import { APIcall, currentUser, permissionGroup, permissionType, userPermissionsDetails, userView } from "../interfaces";
import UserPermissionGroupView from "./components/UserPermissionGroupView";
import ItemList from "./components/ItemList";
import UserPermissionsView from "./components/UserPermissionsView";
import styled from "@emotion/styled";
import {theme} from "../theme"

interface Props { }

const ManageUserPermissionsPageContainer = styled(Flex) `
  flex-direction: row;
  height: 100rem;
`
const UsersList = styled(Flex) `
  flex-direction: column;
  flex-basis: 25%;
  height: 100rem;
  align-items: center;
  border-right: solid;
  border-width:0.1rem;
  border-color: lightgray;
  background-color: ${theme.colors?.background};
  padding-top: 1rem;
  
`
const PermissionUserView = styled(Flex) `
   flex-basis: 75%;
   height: 100rem;
   margin-left: 1rem;
   margin-right: 1rem;
   flex-direction: column;
`
const UserSectionHeading = styled(Heading) `
  text-align: center; 
  margin: 1rem;
`
const UserSectionText = styled(Text) `
  margin: 1rem;
  line-height: 1.5;
  font-size: 14;
  `
  
  const UserGroupPermissionsSelectionView = styled(Flex) `
  flex-direction: row;
  margin: 1rem;
`
const UserSubHeadingText = styled(Text) `
  line-height: 1.5;
  font-size: 14;
  text-decoration: underline;
  margin-left: 0.2rem;
  margin-right: 1rem;
  margin-top: 0.5rem;
  `
  const UserPermissionPageUpper = styled(Flex) `
  margin: 1rem;
  flex-direction: column;
 `
  const UserPermissionList = styled(Flex) `
  margin: 2rem;
  flex-direction: row;
 `
 
const ManageUserPermissionsPage = (props: Props) => {
  const [users, setUsers] = useState<userView[] | null>(null);
  const [permissionTypes, setPermissionTypes] = useState<permissionType[] | null>(null);
  const [permissionGroups, setPermissionGroups] = useState<permissionGroup[] | null>(null);
  const [user, setUser] = useState<userView | null>(null);
  const [userPermissionDetails, setUserPermissionDetails] = useState<userPermissionsDetails | null>(null);
  const [currUser, setCurrUser] = useState<currentUser|null>(null); 

  const handleUserSelect = (selectedUser: userView) => {
    setUser(selectedUser);
    const userPermissionsAPIcall: APIcall = {
      method: 'GET',
      path: 'admin/permissions/user/get_permissions?' + new URLSearchParams({ user_id: selectedUser.user_id.toString() }),
      body: null,
    }
    ApiFetch<userPermissionsDetails>(userPermissionsAPIcall)
      .then((userPermissionDetails) => {
        setUserPermissionDetails(userPermissionDetails);
      })
  }
  
  const handleAddUserPermission = (permission_id: number) => {
    handleSetUserPermission(permission_id, true);
  }

  const handleRemoveUserPermission = (permission_id: number) => {
    handleSetUserPermission(permission_id, false);
  }

  const invokeSetUserPermissions = (requestBody: { user_id: number, permissions: { permission_id: number, value?: boolean }[], group_id: number }) => {
    const setUserPermissionsAPIcall: APIcall = {
      method: 'PUT',
      path: 'admin/permissions/user/set_permissions',
      body: requestBody,
    }
    ApiFetch<{ permissions: permissionType[] }>(setUserPermissionsAPIcall);
  }

  const handleSetUserPermission = (permissionId: number, value: boolean) => {
    if (user !== null && userPermissionDetails !== null) {
      const updatedUserPermissions = userPermissionDetails.permissions.map(permission => ({ permission_id: permission.permission_id, value: permission.permission_id === permissionId ? value : permission.value }));
      setUserPermissionDetails({ permissions: updatedUserPermissions, group_id: userPermissionDetails.group_id });
      invokeSetUserPermissions({ user_id: user.user_id, permissions: updatedUserPermissions, group_id: userPermissionDetails.group_id });
    }
  }
  
  const handleSetUserPermissionGroup = (groupId: number) => {
    if (user !== null && userPermissionDetails !== null) {
      setUserPermissionDetails({ permissions: userPermissionDetails.permissions, group_id: groupId });
      invokeSetUserPermissions({ user_id: user.user_id, permissions: userPermissionDetails.permissions, group_id: groupId });
    }
  }

  useEffect(() => {
    const getAllUsersAPIcall: APIcall = {
      method: 'GET',
      path: 'admin/users/all',
      body: null,
    }
    ApiFetch<{ users: userView[] }>(getAllUsersAPIcall)
      .then(({ users }) => {
        setUsers(users);
      })

    const permissionGroupAPIcall: APIcall = {
      method: 'GET',
      path: 'admin/permissions/groups/list',
      body: null,
    }
    ApiFetch<{ groups: permissionGroup[] }>(permissionGroupAPIcall).then(({ groups }) => {
      setPermissionGroups(groups);
    });

    const permissionsListAPIcall: APIcall = {
      method: 'GET',
      path: 'admin/permissions/list_permissions',
      body: null,
    }
    ApiFetch<{ permissions: permissionType[] }>(permissionsListAPIcall)
      .then(({ permissions }) => {
        setPermissionTypes(permissions);
      })
      setCurrUser(getCurrentUser()); 
  }, []);
  
  return (
    <ManageUserPermissionsPageContainer>
      <UsersList>
        {users !== null ? <ItemList<userView> selectedItem={user} items={users} getItemKey={(user) => user.user_id} getItemLabel={(user) => `${user.name_first} ${user.name_last}`}  onClickItem={handleUserSelect} /> : null}
      </UsersList>

      <PermissionUserView>
        { userPermissionDetails !== null && permissionGroups  ? 
        <UserPermissionPageUpper> 
        <UserSectionHeading> User Permissions Page </UserSectionHeading>
        <UserSectionText>Need to change a user's group permissions? Or maybe you need provide the user with custom permissions? You can edit the permissions of this user at any time using the checkboxes below!</UserSectionText>
        <UserGroupPermissionsSelectionView>
        <UserSubHeadingText> Group Permissions allocated: </UserSubHeadingText>
        <UserPermissionGroupView shouldDisable = {currUser?.user_id === user?.user_id} groupId={userPermissionDetails.group_id} permissionGroups={permissionGroups} onPermissionGroupChange={handleSetUserPermissionGroup}></UserPermissionGroupView>
        </UserGroupPermissionsSelectionView>
        </UserPermissionPageUpper>: null}
        
        {user !== null && userPermissionDetails !== null && permissionTypes !== null && permissionGroups !== null ? 
        <UserPermissionList>
        <UserPermissionsView shouldDisable = {currUser?.user_id === user.user_id} permissionHolder={userPermissionDetails} permissionTypes={permissionTypes} onAddUserPermission={handleAddUserPermission} onRemoveUserPermission={handleRemoveUserPermission}  />  
        </UserPermissionList>
        : null}
      </PermissionUserView>
    </ManageUserPermissionsPageContainer>
  );
};

export default ManageUserPermissionsPage;