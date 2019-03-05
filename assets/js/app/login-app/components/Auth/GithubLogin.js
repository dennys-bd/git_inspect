import React from 'react';

const GithubLogin = () => {
  const CLIENT_ID = () => '57724be44134521aa9fd';
  const REDIRECT_URI = () => 'http://localhost:8000/callback';
  // const PROPS = () => props;

  return (
    <a
      className="ui basic button"
      href={`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID()}&scope=read:user,user:email,repo:status,admin:repo_hook&redirect_uri=${REDIRECT_URI()}`}
    >
      <i className="github icon" />
      Sign in with github
    </a>
  );
};

export default GithubLogin;
