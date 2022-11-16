import { useEffect, useState } from 'react'
import { Button, Flex, Heading, Input, Text } from 'theme-ui'
import { ApiFetch } from '../App'
import { APIcall, permissionGroup, permissionType } from '../interfaces'
import ItemList from './components/ItemList'
import UserPermissionGroupView from './components/UserPermissionGroupView'
import UserPermissionsView from './components/UserPermissionsView'
import styled from "@emotion/styled";
import { theme } from '../theme';
import GroupPermissionsView from './components/GroupPermissionView'


type Props = {}

const ManageGroupPermissionsPageContainer = styled(Flex) `
  flex-direction: row;
  height: 90vh;
  overflow:auto;
`
const PermissionGroupsList = styled(Flex) `
  flex-direction: column;
  flex-basis: 25%;
  height: 90vh;
  overflow: auto;
  align-items: center;
  border-right: solid;
  border-width:0.1rem;
  border-color: lightgray;
  background-color: ${theme.colors?.background};
  
`

const PermissionGroupView = styled(Flex) `
   flex-basis: 75%;
   height: 90vh;
   overflow:auto;
   margin-left: 1rem;
   margin-right: 1rem;
   flex-direction: column;
`
const CreateGroupButton = styled(Button) `
    height: 3rem;
    width: 16rem;
    margin: 0.2rem;
    text-align: center;
    border-radius: 0.5rem;
    background-color:${theme.colors?.highlight};
    filter: brightness(90%);
    color: black;
    
    &:hover {
      background-color: ${theme.colors?.highlight};
      
    }
`

const SectionHeading = styled(Heading) `
  text-align: center; 
  margin: 1rem;
`
const SectionText = styled(Text) `
  margin: 1rem;
  line-height: 1.5;
  font-size: 14;
`
const NameInputBox = styled(Input) `
  margin: 1rem;
  width: 55rem;  
`
const PermissionList = styled(Flex) `
 margin: 1rem;
 flex-direction: row;
`

const DeletePermissionGroupView = styled(Flex) `
  margin: 1rem;
  flex-direction: column;
  align-items: center;
`

const TransferGroupView = styled(Flex) `
  flex-direction: row;
`
const SubHeadingText = styled(Text) `
  line-height: 1.5;
  font-size: 14;
  text-decoration: underline;
  margin-left: 0.2rem;
  margin-right: 1rem;
  `
  const DeletePermissionGroupButton = styled(Button)`
  height: 3rem; 
  width: 10rem;
  border: none;
  border-radius: 0%;
  margin: 1rem;
  box-sizing: border-box;
  color: black;
  border-radius: 0.5rem;
  background-color:${theme.colors?.highlight};
  filter: brightness(90%);
  
  &.sidebar-button-clicked {
    background-color:lightgray;
  }
  
  &:hover{
    background-color: ${theme.colors?.highlight};
    filter: brightness(100%);
  
  }
  `
const CreateBoxButtonView = styled(Flex) `
  margin-top: 0.9rem;
`
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
    <ManageGroupPermissionsPageContainer>
      <PermissionGroupsList>
      <CreateBoxButtonView>
      <CreateGroupButton onClick={handleCreateGroup}>Create Group</CreateGroupButton>
      </CreateBoxButtonView>
        {permissionGroups !== null ? <ItemList<permissionGroup> selectedItem={selectedPermissionGroup} items={permissionGroups} getItemKey={(permissionGroup) => permissionGroup.group_id} getItemLabel={(permissionGroup) => permissionGroup.name} onClickItem={(permissionGroup) => {
          setSelectedPermissionGroup(permissionGroup);
        }} /> : null}
      </PermissionGroupsList>
      
      
      <PermissionGroupView>
        {selectedPermissionGroup && permissionTypes && permissionGroups ?
          <PermissionGroupView>
          <SectionHeading> GROUP NAME </SectionHeading>
          <SectionText>This the name of the permission group. Need to change the name? Type the new name of your group in the box below! </SectionText>
          <Flex sx={{ flexDirection: 'row'}}>
            <NameInputBox disabled = {selectedPermissionGroup.group_id === 1} value={selectedPermissionGroup.name} onChange={(event) => handleSetGroupName(event.target.value)}></NameInputBox>
          </Flex>
          
          <SectionHeading>PERMISSIONS</SectionHeading>
          <SectionText>Need to set up the permissions of a group? Or maybe the permissions have changed? You can use the list below to maintain the permissions of the selected group!</SectionText>
            <PermissionList>
            <GroupPermissionsView shouldDisable = {selectedPermissionGroup.group_id === 1} permissionTypes={permissionTypes} permissionHolder={selectedPermissionGroup} onAddUserPermission={handleAddPermission} onRemoveUserPermission={handleRemovePermission} />
            </PermissionList>
            
            
            <SectionHeading> DELETE PERMISSION GROUP </SectionHeading>
            <SectionText>Don't need this permission group anymore? 
            You can delete this group by pressing the delete button below. 
            Just don't forget to transfer the members to another permission group before you say goodbye!</SectionText>
            <DeletePermissionGroupView>    
            <TransferGroupView>
            <SubHeadingText>Transfer members of this group to : </SubHeadingText>
            <UserPermissionGroupView shouldDisable = {selectedPermissionGroup.group_id === 1} groupId={transferGroupId} onPermissionGroupChange={(groupId) => setTransferGroupId(groupId)} permissionGroups={permissionGroups}></UserPermissionGroupView>
            </TransferGroupView>
            <DeletePermissionGroupButton  disabled = {selectedPermissionGroup.group_id === 1} onClick={handleDeleteGroup}>Delete Group</DeletePermissionGroupButton>
          </DeletePermissionGroupView>
          </PermissionGroupView>
          : null}
          </PermissionGroupView>
    </ManageGroupPermissionsPageContainer>
  )
}

export default ManageGroupPermissionsPage