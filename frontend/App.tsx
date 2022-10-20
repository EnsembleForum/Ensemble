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
  console.log(requestOptions);
  if (!apiCall.customUrl) {
    apiCall.customUrl = SERVER_PATH;
  }
  return new Promise((resolve, reject) => {
    fetch(`${apiCall.customUrl}${apiCall.path}`, requestOptions)
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
        console.log(err);
        alert(err);
      });
  });
}

export function setToken(value: string) {
  console.log("get: " + window.localStorage.getItem("token"))
  window.localStorage.setItem("token", value);
  console.log("set: " + window.localStorage.getItem("token"))
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
        <Route path='/admin' element={<AdminPage page={'initialise_forum'} />} />
        <Route path='/login' element={<LoginPage />} />
        <Route path='/register' element={<RegisterPage />} />
        <Route path='/password_reset' element={<PasswordResetPage />} />
        <Route path='/profile' element={<UserProfilePage userId={0} />} />
        <Route path='/main' element={<MainPage page="browse" />} />
        <Route path='/admin/registerusers' element={<UsersRegisterPage />} />
      </Routes>
    </Router>
  );
}
export default PassThrough;

