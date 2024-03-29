import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SERVER_PATH } from './constants';
import { APIcall, currentUser, requestOptions } from './interfaces';
import AdminPage from './pages/AdminPage';
import BrowsePage from './pages/BrowsePage';
import InitPage from './pages/InitPage';
import LoginPage from './pages/LoginPage';
import TaskboardPage from './pages/TaskboardPage';
import UserProfilePage from './pages/UserProfilePage';
import NotificationsPage from './pages/NotificationsPage';

export function ApiFetch<T>(apiCall: APIcall) {
  const requestOptions: requestOptions = {
    method: apiCall.method,
    headers: { 'Content-Type': 'application/json' },
  };
  if (apiCall.body) { requestOptions.body = JSON.stringify(apiCall.body); }
  let newparams = '';
  if (apiCall.params) {
    newparams = '?' + (new URLSearchParams(apiCall.params)).toString();
  }
  
  let token = null;
  try {
    token = getCurrentUser().token;
  } catch {}
  if (token !== null) { requestOptions.headers.Authorization = `Bearer ${token}`; }
  // console.log(requestOptions);
  if (!apiCall.customUrl) {
    apiCall.customUrl = SERVER_PATH;
  }
  return new Promise<T>((resolve, reject) => {
    fetch(`${apiCall.customUrl}${apiCall.path}${newparams}`, requestOptions)
      .then((response) => {
        if (response.status === 200) {
          response.json().then(data => {
            resolve(data);
          });
        } else {
          response.json().then(errorMsg => {
            alert(errorMsg.code + ": " + errorMsg.description);
            reject(errorMsg);
          });
        }
      })
      .catch((err) => {
        alert(err);
        console.log(err);
      });
  });
}
export function setCurrentUser(currentUser: currentUser | null) {
  window.localStorage.setItem("user", JSON.stringify(currentUser));
  window.dispatchEvent(new Event("storage"));
}
export function getCurrentUser(): currentUser {
  const ret = JSON.parse(window.localStorage.getItem("user") as string);
  return ret;
}

export function getPermission(id : number) {
  if (getCurrentUser()) {
    const userPermissions = getCurrentUser().permissions;
    for (const permission of userPermissions) {
      if (permission.permission_id === id ) {
        return permission.value;
      }
    }
  }
  return false;
}

export function getLoggedIn() {
  if (getCurrentUser()) {
    return getCurrentUser().logged_in;
  }
  return false;
}

function PassThrough() {
  const [firstRun, setFirstRun] = React.useState<boolean>(true);
  const [update, setUpdate] =  React.useState<boolean>(true);
  const api: APIcall = {
    method: "GET",
    path: "admin/is_first_run",
  }
  ApiFetch(api).then((data) => {
    const first = data as {value: boolean};
    setFirstRun(first.value);
  })
  window.addEventListener('storage', () => {
    setUpdate(!update);
    setFirstRun(false);
  });

  React.useEffect(() => {}, [update]);
  return (
    <Router>
      <Routes>
        {firstRun ? (
          <><Route path="/" element={<Navigate to="/admin/init" />}></Route>
          <Route path='/admin/init' element={<InitPage />} /></>
        ) : (
          <>
          <Route path="/" element={<Navigate to="/browse" />}></Route>
          <Route path='/admin/init' element={ getLoggedIn() ? <Navigate to="/browse" /> : <Navigate to="/login" />} />
          <Route path='/login' element={<LoginPage />} />
          <Route path='/profile' element={<UserProfilePage />} />
          <Route path='/browse' element={<BrowsePage />}/>
          {getPermission(20) ? <Route path='/taskboard' element={<TaskboardPage />} /> : <></>}
          {getPermission(40)  ? <Route path='/admin' element={<AdminPage page={"register_users"} />} /> : <></>}
          <Route path='/notifications' element={<NotificationsPage />} />
          </>
        )}
      </Routes>
    </Router>
  )  
}
export default PassThrough;