import React from 'react';
import ReactDOM from 'react-dom';
import GitHubLogin from 'react-github-login';

const onSuccess = response => console.log(response);
const onFailure = response => console.error(response);

ReactDOM.render(
  <GitHubLogin
    clientId="57724be44134521aa9fd"
    onSuccess={onSuccess}
    onFailure={onFailure}
  />,
  document.getElementById('react-app'),
);
