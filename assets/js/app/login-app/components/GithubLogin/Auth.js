import React from 'react';
import { hot } from 'react-hot-loader';
import STATUS from './status';
import GithubLogin from './GithubLogin';

class Auth extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      status: STATUS.INITIAL,
      token: null,
    };
  }

  componentDidMount() {
    const code = window.location.href.match(/\?code=(.*)/)
    && window.location.href.match(/\?code=(.*)/)[1];
    if (code) {
      this.setState({ status: STATUS.LOADING });
      fetch(`https://git-inspect-gatekeeper.herokuapp.com/authenticate/${code}`)
        .then(response => response.json())
        .then(({ token }) => {
          this.setState({
            token,
            status: STATUS.FINISHED_LOADING,
          });
        });
    }
  }

  render() {
    console.log(this.state.status);
    if (this.state.status === STATUS.INITIAL) {
      return <GithubLogin />;
    }
    if (this.state.status === STATUS.LOADING) {
      return (
        <div className="ui segment">
          <div className="ui active inverted dimmer">
            <div className="ui text loader">Loading</div>
          </div>
          <p />
        </div>
      );
    }
    return <h1>{this.state.token}</h1>;
  }
}

export default hot(module)(Auth);
