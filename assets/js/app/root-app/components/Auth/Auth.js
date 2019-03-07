import React from 'react';
import PropTypes from 'prop-types';
import STATUS from './Status';
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
    const { token } = this.state;
    if (token != null) {
      this.setState({
        status: STATUS.AUTHENTICATED,
      });
    }
  }

  render() {
    let element;
    const { status, token } = this.state;
    const { authenticate } = this.props;

    if (status === STATUS.AUTHENTICATED) {
      element = <UserValidation token={token} authenticate={authenticate} />;
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

Auth.defaultProps = {
  authenticate: () => {},
};

Auth.propTypes = {
  authenticate: PropTypes.func,
};

export default Auth;
