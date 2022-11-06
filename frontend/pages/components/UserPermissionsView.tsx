import React, { ReactElement } from 'react'
import { Flex, Checkbox, Heading, Label } from 'theme-ui'
import { permissionType, userPermissionsDetails, userView } from "../../interfaces"
type Props = {
  userPermissionsDetails: userPermissionsDetails,
  permissionTypes: permissionType[],
  onAddUserPermission: (permissionId: number) => void,
  onRemoveUserPermission: (permissionId: number) => void
}

const UserPermissionsView = ({ userPermissionsDetails, permissionTypes, onAddUserPermission, onRemoveUserPermission }: Props) => {
  const userPermissions = userPermissionsDetails.permissions.reduce(
    (previousPermissionIds, permission) => {
      if (permission.value) {
        previousPermissionIds.add(permission.permission_id);
      }
      return previousPermissionIds;
    }, new Set<number>());
  return (
    <Flex sx={{ flexDirection: 'column' }}>
      {permissionTypes.map((permissionType: permissionType): ReactElement => {
        return <Flex key={permissionType.permission_id}>
          <Label>
            <Checkbox
              checked={userPermissions?.has(permissionType.permission_id)}
              onChange={(event) => {
                event.target.checked ?
                  onAddUserPermission(permissionType.permission_id)
                  : onRemoveUserPermission(permissionType.permission_id);
              }}>
            </Checkbox>
            {permissionType.name}
          </Label>
        </Flex>
      })}
    </Flex>
  )
}

export default UserPermissionsView