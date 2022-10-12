import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SERVER_PATH } from './constants';
import { requestOptions } from './interfaces';
import AdminPage from './pages/AdminPage';
import BrowsePage from './pages/BrowsePage';
import InitPage from './pages/InitPage';
import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';
import PasswordResetPage from './pages/PasswordResetPage';
import RegisterPage from './pages/RegisterPage';
import TaskboardPage from './pages/TaskboardPage';

export function ApiFetch (method : string, path : string, token : string | null, body? : object, customUrl?: string) {
  const requestOptions : requestOptions = {
    method: method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body !== null) { requestOptions.body = JSON.stringify(body); }
  if (token !== null) { requestOptions.headers.Authorization = `Bearer ${token}`; }
  console.log(JSON.stringify(requestOptions));
  if (!customUrl) {
    customUrl = SERVER_PATH;
  }
  return new Promise((resolve, reject) => {
    fetch(`${customUrl}${path}`, requestOptions)
      .then((response) => {
        if (response.status === 400 || response.status === 403) {
          response.json().then((errorMsg) => {
            console.log(errorMsg.error);
            alert(errorMsg.error);
          });
        } else if (response.status === 200) {
          response.json().then(data => {
            resolve(data);
          });
        }
      })
      .catch((err) => console.log(err));
  });
}


function PassThrough () {
  return (
    <Router>
        <Routes>
          <Route path = "/" element={<Navigate to="/init" />}></Route>
          <Route path='/init' element={<InitPage/>} />
          <Route path='/admin' element={<AdminPage/>} />
          <Route path='/auth/login' element={<LoginPage/>} />
          <Route path='/auth/register' element={<RegisterPage/>} />
          <Route path='/auth/password_reset' element={<PasswordResetPage/>} />
          <Route path='/main' element={<MainPage page = "browse"/>} />
        </Routes>
    </Router>
  );
}
export default PassThrough;

