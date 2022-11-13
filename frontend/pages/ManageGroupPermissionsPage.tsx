import { useEffect, useState } from 'react'
import { Button, Flex, Input } from 'theme-ui'
import { ApiFetch } from '../App'
import { APIcall, permissionGroup, permissionType } from '../interfaces'
import ItemList from './components/ItemList'
import UserPermissionGroupView from './components/UserPermissionGroupView'
import UserPermissionsView from './components/UserPermissionsView'

type Props = {}

const ManageGroupPermissionsPage = (props: Props) => {

  const [permissionTypes, setPermissionTypes] = useState<permissionType[] | null>(null);
  const [permissionGroups, setPermissionGroups] = useState<permissionGroup[] | null>(null);
  const [selectedPermissionGroup, setSelectedPermissionGroup] = useState<permissionGroup | null>(null);
  const [transferGroupId, setTransferGroupId] = useState<number | null>(null);

  useEffect(() => {
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

  const handleAddPermission = (permission_id: number) => {
    handleSetPermission(permission_id, true);
  }

  const handleRemovePermission = (permission_id: number) => {
    handleSetPermission(permission_id, false);
  }

  const invokeSetGroupPermissions = (requestBody: permissionGroup) => {
    const setGroupPermissionsAPIcall: APIcall = {
      method: 'PUT',
      path: '/admin/permissions/groups/edit',
      body: requestBody,
    }
    ApiFetch<void>(setGroupPermissionsAPIcall);
  }

  const handleSetPermission = (permissionId: number, value: boolean) => {
    if (selectedPermissionGroup !== null) {
      const updatedPermissions = selectedPermissionGroup.permissions.map(permission => ({ permission_id: permission.permission_id, value: permission.permission_id === permissionId ? value : permission.value }));
      const updatedPermissionGroup = { group_id: selectedPermissionGroup.group_id, name: selectedPermissionGroup.name, permissions: updatedPermissions };
      setUpdatedPermissionGroup(updatedPermissionGroup);
    }
  };

  const setUpdatedPermissionGroup = (updatedPermissionGroup: permissionGroup) => {
    const updatedPermissionGroups = permissionGroups?.map(permissionGroup => permissionGroup.group_id === updatedPermissionGroup.group_id ? updatedPermissionGroup : permissionGroup) ?? null;
    setSelectedPermissionGroup(updatedPermissionGroup);
    setPermissionGroups(updatedPermissionGroups);
    invokeSetGroupPermissions(updatedPermissionGroup);
  }

  const handleSetGroupName = (updatedGroupName: string) => {
    if (selectedPermissionGroup !== null) {
      const updatedPermissionGroup = { ...selectedPermissionGroup, name: updatedGroupName };
      setUpdatedPermissionGroup(updatedPermissionGroup);
    }
  }

  const handleCreateGroup = () => {
    if (permissionGroups && permissionTypes) {
      const newGroup: Omit<permissionGroup, 'group_id'> = { name: 'New Group', permissions: permissionTypes.map(permissionType => ({ permission_id: permissionType.permission_id, value: false })) };
      const setGroupPermissionsAPIcall: APIcall = {
        method: 'POST',
        path: '/admin/permissions/groups/create',
        body: newGroup,
      }
      ApiFetch<{ group_id: number }>(setGroupPermissionsAPIcall).then(({ group_id }) => {
        setPermissionGroups([...permissionGroups, { ...newGroup, group_id }])
      })
    }
  }

  const handleDeleteGroup = () => {
    if (selectedPermissionGroup && permissionGroups && transferGroupId != null) {
      const remainingPermissionGroups = permissionGroups.filter(permissionGroup => permissionGroup.group_id !== selectedPermissionGroup.group_id);
      setPermissionGroups(remainingPermissionGroups);
      setSelectedPermissionGroup(null);
      const setGroupPermissionsAPIcall: APIcall = {
        method: 'DELETE',
        path: '/admin/permissions/groups/remove?' + new URLSearchParams({ group_id: selectedPermissionGroup.group_id.toString(), transfer_group_id: transferGroupId.toString() }),
        body: null
      }
      ApiFetch<void>(setGroupPermissionsAPIcall);
    }
  }

  return (
    <Flex sx={{ flexDirection: 'row' }}>
      <Flex sx={{ flexDirection: 'row', flexGrow: 1 }}>
        <Button onClick={handleCreateGroup}>Create Group</Button>
        {permissionGroups !== null ? <ItemList<permissionGroup> items={permissionGroups} getItemKey={(permissionGroup) => permissionGroup.group_id} getItemLabel={(permissionGroup) => permissionGroup.name} onClickItem={(permissionGroup) => {
          setSelectedPermissionGroup(permissionGroup);
        }} /> : null}
      </Flex>

      <Flex sx={{ flexDirection: 'row', flexGrow: 4 }}>
        {selectedPermissionGroup && permissionTypes && permissionGroups ?
          <Flex>
            <Input value={selectedPermissionGroup.name} onChange={(event) => handleSetGroupName(event.target.value)}></Input>
            <UserPermissionsView permissionTypes={permissionTypes} permissionHolder={selectedPermissionGroup} onAddUserPermission={handleAddPermission} onRemoveUserPermission={handleRemovePermission} />
            <Button onClick={handleDeleteGroup}>Delete Group</Button>
            <UserPermissionGroupView groupId={transferGroupId} onPermissionGroupChange={(groupId) => setTransferGroupId(groupId)} permissionGroups={permissionGroups}></UserPermissionGroupView>
          </Flex>
          : null}
      </Flex>
    </Flex>
  )
}

export default ManageGroupPermissionsPage