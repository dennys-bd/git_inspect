import React from 'react';
import GitHubLogin from 'react-github-login';

const GithubLogin = () => {
  const onSuccess = response => console.log(response);
  const onFailure = response => console.error(response);

  return (
    <GitHubLogin
      clientId="57724be44134521aa9fd"
      onSuccess={onSuccess}
      onFailure={onFailure}
    />
  );
};


// export default GithubLogin;
// import { Button, FormGroup, FormControl, ControlLabel } from "react-bootstrap";

// <div className="Login">
// <form onSubmit={this.handleSubmit}>
//   <Button
//     block
//     bsSize="large"
//     type="submit"
//   >
//   Login
//   </Button>
// </form>
// </div>,
