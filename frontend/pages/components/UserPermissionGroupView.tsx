import styled from '@emotion/styled'
import { Select } from 'theme-ui'
import { permissionGroup } from '../../interfaces'

type Props = {
  groupId: number|null,
  permissionGroups: permissionGroup[],
  onPermissionGroupChange: (groupId: number) => void,
  shouldDisable : boolean,
}

const StyledSelect = styled(Select) `
  width: 16rem;
`
const UserPermissionGroupView = ({groupId , permissionGroups, onPermissionGroupChange, shouldDisable}: Props) => {
  return (
    <div>
    <StyledSelect  disabled = {shouldDisable} value={groupId?.toString()} onChange={(event) => onPermissionGroupChange(Number(event.target.value))}>
      {permissionGroups.map((group) => <option value={group.group_id}>{group.name}</option>)}
    </StyledSelect></div>
  )
}

export default UserPermissionGroupView