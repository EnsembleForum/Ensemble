
import React, { useState } from 'react'
import {Flex, Button} from "theme-ui" 
import ManageGroupPermissionsPage from './ManageGroupPermissionsPage'
import ManageUserPermissionsPage from './ManageUserPermissionsPage'

enum managePermissionPage {
  groups, 
  users
}
type Props = {}

const ManagePermissionsPage = (props: Props) => {
const [currPage, setCurrPage] = useState<managePermissionPage>(managePermissionPage.groups)
 
const getCurrPermissionPage = (currentPage:managePermissionPage) => {
  if(currentPage === managePermissionPage.groups) {
   return <ManageGroupPermissionsPage/>
  } else {
    return <ManageUserPermissionsPage/>
  }
}

const onPageSelection = (selectedPage:managePermissionPage) => {
  setCurrPage(selectedPage); 
}
  return (
    <Flex sx={{flexDirection: 'row'}} >
      
      <Flex sx={{flexDirection: 'column', flexGrow: 1}} >
        <Button onClick={()=>onPageSelection(managePermissionPage.groups)}>Groups</Button>
        <Button onClick={()=>onPageSelection(managePermissionPage.users)}> Users </Button>
      </Flex>
      
      <Flex sx={{flexDirection:'column', backgroundColor: "yellow", flexGrow: 5}}>
       {getCurrPermissionPage(currPage)}
      </Flex>
    </Flex>
  )
}

export default ManagePermissionsPage