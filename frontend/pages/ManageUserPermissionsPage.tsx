import { useEffect, useState } from "react";
import { Flex } from "theme-ui";
import { ApiFetch } from "../App";
import { APIcall, permissionGroup, permissionType, userPermissionsDetails, userView } from "../interfaces";
import UserPermissionGroupView from "./components/UserPermissionGroupView";
import ItemList from "./components/ItemList";
import UserPermissionsView from "./components/UserPermissionsView";

interface Props { }



const ManageUserPermissionsPage = (props: Props) => {
  const [users, setUsers] = useState<userView[] | null>(null);
  const [permissionTypes, setPermissionTypes] = useState<permissionType[] | null>(null);
  const [permissionGroups, setPermissionGroups] = useState<permissionGroup[] | null>(null);
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
  }, []);

  return (
    <Flex sx={{ flexDirection: 'row' }}>
      <Flex sx={{ flexDirection: 'row', flexGrow: 1 }}>
        {users !== null ? <ItemList<userView> items={users} getItemKey={(user) => user.user_id} getItemLabel={(user) => `${user.name_first} ${user.name_last}`}  onClickItem={handleUserSelect} /> : null}
      </Flex>

      <Flex sx={{ flexDirection: 'row', flexGrow: 4 }}>
        { userPermissionDetails !== null && permissionGroups  ? <UserPermissionGroupView groupId={userPermissionDetails.group_id} permissionGroups={permissionGroups} onPermissionGroupChange={handleSetUserPermissionGroup}></UserPermissionGroupView> : null}
        {user !== null && userPermissionDetails !== null && permissionTypes !== null && permissionGroups !== null ? <UserPermissionsView permissionHolder={userPermissionDetails} permissionTypes={permissionTypes} onAddUserPermission={handleAddUserPermission} onRemoveUserPermission={handleRemoveUserPermission}  /> : null}
      </Flex>
    </Flex>
  );
};

export default ManageUserPermissionsPage;