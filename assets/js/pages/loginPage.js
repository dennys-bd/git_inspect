import React from 'react';
import ReactDOM from 'react-dom';
import Auth from '../app/login-app';

const elem = document.getElementById('auth-app');

if (elem != null) {
  ReactDOM.render(<Auth />, elem);
}
