import React from 'react';
import { hot } from 'react-hot-loader';
import STATUS from './status';
import GithubLogin from './GithubLogin';
import UserValidation from './UserValidation';

import './style.scss';

class Auth extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      status: STATUS.INITIAL,
      token: localStorage.getItem('token'),
    };
  }

  componentDidMount() {
    if (this.state.token != null) {
      this.setState({
        status: STATUS.AUTHENTICATED,
      });
    }
  }

  render() {
    let element;

    if (this.state.status === STATUS.AUTHENTICATED) {
      element = <UserValidation token={this.state.token} />;
    } else {
      element = <GithubLogin />;
    }
    return (
      <div className="outer">
        <div className="middle">
          <h2 className="center">Login</h2>
          {element}
        </div>
      </div>
    );
  }
}

export default hot(module)(Auth);
