import React from 'react';

const GithubLogin = () => {
  const CLIENT_ID = () => process.env.CLIENT_ID || '57724be44134521aa9fd';

  return (
    <a
      className="ui basic button"
      href={`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID()}&scope=read:user,user:email,repo:status,admin:repo_hook`}
    >
      <i className="github icon" />
      Sign in with github
    </a>
  );
};

export default GithubLogin;
