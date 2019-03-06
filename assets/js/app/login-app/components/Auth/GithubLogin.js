import React from 'react';


const GithubLogin = () => {
  const CLIENT_ID = () => process.env.CLIENT_ID || '57724be44134521aa9fd';

  const SubmitHandler = (e) => {
    e.preventDefault();
    window.location.replace(`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID()}&scope=read:user,user:email,repo:status,admin:repo_hook`);
  };

  return (
    <form className="ui container center" onSubmit={SubmitHandler}>
      <div className="ui segment">
        <button type="submit" className="ui basic button">
          <i className="github icon" />
          Sign in with github
        </button>
      </div>
    </form>
  );
};

export default GithubLogin;
