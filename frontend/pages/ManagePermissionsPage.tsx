
import React, { useState } from 'react'
import { Flex, Button } from "theme-ui"
import ManageGroupPermissionsPage from './ManageGroupPermissionsPage'
import ManageUserPermissionsPage from './ManageUserPermissionsPage'
import styled from "@emotion/styled";
import { theme } from '../theme';

enum managePermissionPage {
  groups,
  users
}
type Props = {}


const SidebarButton = styled(Button)`
height: 3rem; 
width: 7rem;
border: none;
border-radius: 0%;
margin-top: 1rem;
box-sizing: border-box;
background-color:${theme.colors?.muted};
color: black;
border-radius: 0.5rem;

&.sidebar-button-clicked {
  background-color:lightgray;
}

&:hover{
  background-color: ${theme.colors?.highlight};
}
`

const PermissionsPageContainer = styled(Flex) `
  flex-direction: row;
  width: 100rem;
  height: 100rem;
`

const SideBar = styled(Flex) `
  flex-direction: column; 
  flex-basis: 18%; 
  height: 100rem;
  align-items: center; 
  background-color: ${theme.colors?.muted};
  border-right: solid;
  border-width:0.1rem;
  border-color: lightgray;

`

const PermissionView = styled(Flex) `
flex-direction: column;
flex-basis: 83%;
height: 100rem;
`

const ManagePermissionsPage = (props: Props) => {
  const [currPage, setCurrPage] = useState<managePermissionPage>(managePermissionPage.groups)

  const getCurrPermissionPage = (currentPage: managePermissionPage) => {
    if (currentPage === managePermissionPage.groups) {
      return <ManageGroupPermissionsPage />
    } else {
      return <ManageUserPermissionsPage />
    }
  }

  const onPageSelection = (selectedPage: managePermissionPage) => {
    setCurrPage(selectedPage);
  }
  return (
    <PermissionsPageContainer>

      <SideBar >
        <SidebarButton className={currPage === managePermissionPage.groups ? 'sidebar-button-clicked' : ''} onClick={() => onPageSelection(managePermissionPage.groups)}>Groups</SidebarButton>
        <SidebarButton className={currPage === managePermissionPage.users ? 'sidebar-button-clicked' : ''} onClick={() => onPageSelection(managePermissionPage.users)}> Users </SidebarButton>
      </SideBar>

      <PermissionView>
        {getCurrPermissionPage(currPage)}
      </PermissionView>
    </PermissionsPageContainer>
  )
}

export default ManagePermissionsPage