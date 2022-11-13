import { Select } from 'theme-ui'
import { permissionGroup, userPermissionsDetails } from '../../interfaces'

type Props = {
  groupId: number|null,
  permissionGroups: permissionGroup[],
  onPermissionGroupChange: (groupId: number) => void
}

const UserPermissionGroupView = ({groupId , permissionGroups, onPermissionGroupChange}: Props) => {
  return (
    <div>
    <Select  value={groupId} onChange={(event) => onPermissionGroupChange(Number(event.target.value))}>
      {permissionGroups.map((group) => <option value={group.group_id}>{group.name}</option>)}
    </Select></div>
  )
}

export default UserPermissionGroupView