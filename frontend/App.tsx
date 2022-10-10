import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { SERVER_PATH } from './constants';
import { requestOptions } from './interfaces';
import BrowsePage from './pages/BrowsePage';
import LoginPage from './pages/LoginPage';
import PasswordResetPage from './pages/PasswordResetPage';
import RegisterPage from './pages/RegisterPage';
import TaskboardPage from './pages/TaskboardPage';

export function ApiFetch (method : string, path : string, token : string, body? : string) {
  const requestOptions : requestOptions = {
    method: method,
    headers: { 'Content-Type': 'application/json' }
  };
  if (body !== null) { requestOptions.body = JSON.stringify(body); }
  if (token !== null) { requestOptions.headers.Authorization = `Bearer ${token}`; }
  return new Promise((resolve, reject) => {
    fetch(`${SERVER_PATH}${path}`, requestOptions)
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
          <Route path = "/" element={<Navigate to="/auth/login" />}></Route>
          <Route path='/auth/login' element={<LoginPage/>} />
          <Route path='/auth/register' element={<RegisterPage/>} />
          <Route path='/auth/password_reset' element={<PasswordResetPage/>} />
          <Route path='/browse' element={<BrowsePage/>} />
          <Route path='/taskboard' element={<TaskboardPage/>} />
        </Routes>
    </Router>
  );
}
export default PassThrough;

