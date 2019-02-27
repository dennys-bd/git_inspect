import React from 'react';

// const Auth = (props) => {
//   const URL = () => 'https://git-inspect-gatekeeper.herokuapp.com/';

//   fetch(URL + props.code)
//   .then(response => response.json())
// };

class Auth extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      token: null,
    };

    this.GithubLogin = this.GithubLogin.bind(this);
  }

  render() {
    return <div className={this.state.token} />;
  }
}
