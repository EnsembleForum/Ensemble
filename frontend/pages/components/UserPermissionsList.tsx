import React from 'react'
import { theme } from '../../theme'
import {Flex} from 'theme-ui'
import {user} from '../../interfaces'

type Props = {users: user[], onClickUser:(user:user)=>void}


const UserPermissionsList = ({users, onClickUser}: Props) => {
  return (
    <Flex sx={{flexDirection:'column'}}>
      {users.map((user: user)=>{
        return <div key={user.user_id} onClick={()=>{onClickUser(user)}}>
        {user.name_first} {user.name_last}
        </div>
      })}
    </Flex>
  )
}

export default UserPermissionsList
