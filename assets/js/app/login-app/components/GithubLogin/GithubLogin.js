import React from 'react';
// import GitHubLogin from 'react-github-login';

// const GithubLogin = () => {
//   const onSuccess = response => console.log(response);
//   const onFailure = response => console.error(response);

//   return (
//     <GitHubLogin
//       className="ui basic button"
//       clientId="57724be44134521aa9fd"
//       onSuccess={onSuccess}
//       onFailure={onFailure}
//     >
//       <i className="github icon" />
//       Sign in with github
//     </GitHubLogin>
//   );
// };


const GithubLogin = () => {
  const CLIENT_ID = () => '57724be44134521aa9fd';
  const REDIRECT_URI = () => 'http://localhost:8000/callback';
  // const PROPS = () => props;

  return (
    <a
      className="ui basic button"
      href={`https://github.com/login/oauth/authorize?client_id=${CLIENT_ID()}&scope=user&redirect_uri=${REDIRECT_URI()}`}
    >
      <i className="github icon" />
      Sign in with github
    </a>
  );
};

export default GithubLogin;
