import styled from '@emotion/styled'
import { ReactElement } from 'react'
import { Checkbox, Flex, Label } from 'theme-ui'
import { permissionHolder, permissionType } from "../../interfaces"
type Props = {
  permissionHolder: permissionHolder,
  permissionTypes: permissionType[],
  onAddUserPermission: (permissionId: number) => void,
  onRemoveUserPermission: (permissionId: number) => void
  shouldDisable: boolean,
}

const StyledCheckbox = styled(Checkbox) `
  margin-bottom: 0.5rem;
  font-size: 14;
`
const GroupPermissionsView = ({ permissionHolder, permissionTypes, onAddUserPermission, onRemoveUserPermission, shouldDisable }: Props) => {
  const userPermissions = permissionHolder.permissions.reduce(
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
            <StyledCheckbox
            disabled= {shouldDisable}
              checked={userPermissions?.has(permissionType.permission_id)}
              onChange={(event) => {
                event.target.checked ?
                  onAddUserPermission(permissionType.permission_id)
                  : onRemoveUserPermission(permissionType.permission_id);
              }}>
            </StyledCheckbox>
            {permissionType.name}
          </Label>
        </Flex>
      })}
    </Flex>
  )
}

export default GroupPermissionsView