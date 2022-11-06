import styled from "@emotion/styled";
import { Flex } from "theme-ui"
import { APIcall, permissionType, userPermissionsDetails, userView } from "../interfaces";
import React, { JSXElementConstructor, MouseEvent, ReactElement, useEffect, useState } from "react";
import UserPermissionsList from "./components/UserPermissionsList";
import { ApiFetch } from "../App";
import UserPermissionsView from "./components/UserPermissionsView";

interface Props { }



const ManagePermissionsPage = (props: Props) => {
  const [users, setUsers] = useState<userView[] | null>(null);
  const [permissionTypes, setPermissionTypes] = useState<permissionType[] | null>(null);
  const [user, setUser] = useState<userView | null>(null);
  const [userPermissionDetails, setUserPermissionDetails] = useState<userPermissionsDetails | null>(null);

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

  const handleSetUserPermission = (permission_id: number, value: boolean) => {
    if (user !== null && userPermissionDetails !== null) {
      const updatedUserPermissions = userPermissionDetails.permissions.map(permission => ({ permission_id: permission.permission_id, value: permission.permission_id === permission_id ? value : permission.value }));
      const updatedUserPermissionDetails: userPermissionsDetails = { permissions: updatedUserPermissions, group_id: userPermissionDetails.group_id };
      setUserPermissionDetails(updatedUserPermissionDetails);
      invokeSetUserPermissions({ user_id: user.user_id, permissions: updatedUserPermissionDetails.permissions, group_id: updatedUserPermissionDetails.group_id });
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

    const permissionsListAPIcall: APIcall = {
      method: 'GET',
      path: 'admin/permissions/list_permissions',
      body: null,
    }
    ApiFetch<{ permissions: permissionType[] }>(permissionsListAPIcall)
      .then(({ permissions }) => {
        setPermissionTypes(permissions);
      })
  }, []);

  return (
    <Flex>
      {users !== null ? <UserPermissionsList users={users} onClickUser={handleUserSelect} /> : null}
      {user !== null && userPermissionDetails !== null && permissionTypes !== null ? <UserPermissionsView userPermissionsDetails={userPermissionDetails} permissionTypes={permissionTypes} onAddUserPermission={handleAddUserPermission} onRemoveUserPermission={handleRemoveUserPermission} /> : null}
    </Flex>
  );
};

export default ManagePermissionsPage;