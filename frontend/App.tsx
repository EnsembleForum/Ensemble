import styled from '@emotion/styled';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SERVER_PATH } from './constants';
import { APIcall, requestOptions } from './interfaces';
import AdminPage from './pages/AdminPage';
import BrowsePage from './pages/BrowsePage';
import InitPage from './pages/InitPage';
import LoginPage from './pages/LoginPage';
import MainPage from './pages/MainPage';
import PasswordResetPage from './pages/PasswordResetPage';
import RegisterPage from './pages/RegisterPage';
import TaskboardPage from './pages/TaskboardPage';
import UserProfilePage from './pages/UserProfilePage';
import UsersRegisterPage from './pages/UsersRegisterPage';

export function ApiFetch(apiCall: APIcall) {
  const requestOptions: requestOptions = {
    method: apiCall.method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (apiCall.body) { requestOptions.body = JSON.stringify(apiCall.body); }
  const token = getToken();
  if (token !== null) { requestOptions.headers.Authorization = `Bearer ${token}`; }
  console.log(JSON.stringify(requestOptions));
  if (!apiCall.customUrl) {
    apiCall.customUrl = SERVER_PATH;
  }
  return new Promise((resolve, reject) => {
    fetch(`${apiCall.customUrl}${apiCall.path}`, requestOptions)
      .then((response) => {
        console.log(response);
        if (response.status === 400 || response.status === 403) {
          response.json().then((errorMsg) => {
            console.log(errorMsg.error);
            alert(errorMsg.error);
            reject(errorMsg);
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

export function setToken(value: string) {
  console.log(value);
  window.localStorage.setItem("token", value);
}
export function getToken(): string | null {
  const token = window.localStorage.getItem("token");
  return token;
}


function PassThrough() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/admin/init" />}></Route>
        <Route path='/admin/init' element={<InitPage />} />
        <Route path='/admin' element={<AdminPage />} />
        <Route path='/auth/login' element={<LoginPage />} />
        <Route path='/auth/register' element={<RegisterPage />} />
        <Route path='/auth/password_reset' element={<PasswordResetPage />} />
        <Route path='/user/profile' element={<UserProfilePage userId={0} />} />
        <Route path='/main' element={<MainPage page="browse" />} />
        <Route path='/admin/users/register' element={<UsersRegisterPage />} />
      </Routes>
    </Router>
  );
}
export default PassThrough;

