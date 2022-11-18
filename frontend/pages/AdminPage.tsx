import styled from "@emotion/styled";
import React from "react";
import { Prettify } from "../global_functions";
import { APIcall, pageList } from "../interfaces";
import { theme } from "../theme";
import AnalyticsPage from "./AnalyticsPage";
import Navbar, { StyledNavbar } from "./components/Navbar";
import ManagePermissionsPage from "./ManagePermissionsPage";
import ManageTagsPage from "./ManageTagsPage";
import UsersRegisterPage from "./UsersRegisterPage";
import { StyledButton } from "./GlobalProps";
import { ApiFetch } from "../App";
import { useSearchParams } from "react-router-dom";


interface Props {
  page: "initialise_forum" | "register_users" | "manage_user_permissions" | "manage_tags"
}

const AdminPanel = styled(StyledNavbar)`
  background-color: white;
  align-items: center;
  justify-content: center;
  a {
    background-color: ${theme.colors?.highlight};
    border-radius: 10px;
    min-width: 60px;
    display: flex;
    justify-content: center;
    &:hover {
      cursor: pointer;
      background-color: ${theme.colors?.highlight};
      filter: brightness(85%);
    }
    &:active {
      background-color: ${theme.colors?.highlight};
      filter: brightness(85%);
    }
  }
`
const Max = styled.div`
  max-height: 100vh;
  overflow: hidden;
`

const AdminPage = (props: Props) => {
  const [currPage, setCurrPage] = React.useState<string>(props.page);
  let [searchParams, setSearchParams] = useSearchParams();
  let pages: pageList = {
    "register_users": <UsersRegisterPage />,
    "analytics": <AnalyticsPage />,
    "manage_user_permissions": <ManagePermissionsPage/>,
    "manage_tags": <ManageTagsPage/>,
  };
  function toggleExamMode() {
    const call : APIcall = {
      method: "PUT",
      path: "admin/exam_mode/toggle"
    }
    ApiFetch(call).then((data) => {
      const d = data as {is_enabled: boolean};
      const da = d.is_enabled ? "true" : "false";
      searchParams.set("exam_mode", da);
      setSearchParams(searchParams);
    })
  }
  return (
    <Max>
      <Navbar page="admin" />
      <AdminPanel>
        {Object.keys(pages).map((key) => {
          let active = '';
          if (key === currPage) {
            active = "active"
          }
          return (<a key={key} style={(key === currPage) ? { filter: "brightness(95%)" } : { filter: "brightness(100%)" }} onClick={(e) => { setCurrPage(key) }}>{Prettify(key)}</a>)
        })}
        <StyledButton onClick={() => {toggleExamMode()}}>Exam Mode</StyledButton>
      </AdminPanel>
      {pages[currPage]}
    </Max>
  )
};

export default AdminPage;