import styled from '@emotion/styled'
import { Select } from 'theme-ui'
import { permissionGroup, userPermissionsDetails } from '../../interfaces'

type Props = {
  groupId: number|null,
  permissionGroups: permissionGroup[],
  onPermissionGroupChange: (groupId: number) => void
}

const StyledSelect = styled(Select) `
  width: 16rem;
`
const UserPermissionGroupView = ({groupId , permissionGroups, onPermissionGroupChange}: Props) => {
  return (
    <div>
    <StyledSelect  value={groupId?.toString()} onChange={(event) => onPermissionGroupChange(Number(event.target.value))}>
      {permissionGroups.map((group) => <option value={group.group_id}>{group.name}</option>)}
    </StyledSelect></div>
  )
}

export default UserPermissionGroupView