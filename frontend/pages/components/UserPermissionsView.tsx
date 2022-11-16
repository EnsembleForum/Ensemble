import styled from '@emotion/styled'
import { ReactElement } from 'react'
import { Checkbox, Flex, Label } from 'theme-ui'
import { permissionHolder, permissionType, userPermission } from "../../interfaces"
type Props = {
  permissionHolder: permissionHolder,
  permissionTypes: permissionType[],
  onSetUserPermission: (permissionId: number, value: boolean | null) => void,
  shouldDisable: boolean,
  groupPermissions: userPermission[],
}

const StyledCheckbox = styled(Checkbox)`
  font-size: 14;
  margin-left: 0.8rem;
  margin-right: 0.8rem;
  
  &.disabledCheckbox {
    opacity: 60%;
    color: lightgrey;
  }
  
`

const StyledLabel = styled.label `
  margin: 0.8rem;
  display: flex;
  flex-direction: row;
  align-items:center;
`
const PermissionNameView = styled(Flex) `
  margin: 1rem;
  justify-content:center ;
`
const PermissionTypeHeading = styled(Flex) `
  flex-direction: row;
`

const PermissionHeading = styled(Flex) `
  margin-left: 1rem;
  text-decoration: underline;
`
const UserPermissionsView = ({ permissionHolder, permissionTypes, onSetUserPermission, shouldDisable, groupPermissions }: Props) => {

  const inheritedPermissions = permissionHolder.permissions.reduce(
    (previousPermissionIds, permission) => {
      if (permission.value == null) {
        previousPermissionIds.add(permission.permission_id);
      }
      return previousPermissionIds;
    }, new Set<number>());

  const groupPermissionSet = groupPermissions.reduce(
    (previousPermissionIds, permission) => {
      if (permission.value) {
        previousPermissionIds.add(permission.permission_id);
      }
      return previousPermissionIds;
    }, new Set<number>());

  const userPermissions = permissionHolder.permissions.reduce(
    (previousPermissionIds, permission) => {
      if (inheritedPermissions.has(permission.permission_id)) {
        if (groupPermissionSet.has(permission.permission_id)) {
          previousPermissionIds.add(permission.permission_id);
        }
      } else if (permission.value) {
        previousPermissionIds.add(permission.permission_id);
      }
      return previousPermissionIds;
    }, new Set<number>());


  return (
    <Flex sx={{ flexDirection: 'column' }}>
           <PermissionTypeHeading>
           <PermissionHeading>Inherited</PermissionHeading> 
           <PermissionHeading> Value </PermissionHeading>
           </PermissionTypeHeading>
      {permissionTypes.map((permissionType: permissionType): ReactElement => {
        return <Flex key={permissionType.permission_id}>
          <StyledLabel>
            <StyledCheckbox
              className = { shouldDisable ? 'disabledCheckbox' : ''}
              disabled={shouldDisable}
              checked={inheritedPermissions?.has(permissionType.permission_id)}
              onChange={(event) => {
                onSetUserPermission(permissionType.permission_id, event.target.checked ? null : userPermissions?.has(permissionType.permission_id))
              }}>
            </StyledCheckbox>
          </StyledLabel>

          <StyledLabel>
            <StyledCheckbox
            className = { inheritedPermissions?.has(permissionType.permission_id) ? 'disabledCheckbox' : ''}
              disabled={shouldDisable || inheritedPermissions?.has(permissionType.permission_id)}
              checked={userPermissions?.has(permissionType.permission_id)}
              onChange={(event) => {
                onSetUserPermission(permissionType.permission_id, event.target.checked)
              }}>
            </StyledCheckbox>
            <PermissionNameView>
            {permissionType.name}
            </PermissionNameView>

          </StyledLabel>
        </Flex>
      })}
    </Flex>
  )
}

export default UserPermissionsView