import React from 'react';
import { hot } from 'react-hot-loader';
import STATUS from './status';
import GithubLogin from './GithubLogin';

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
  //   const code = window.location.href.match(/\?code=(.*)/)
  //   && window.location.href.match(/\?code=(.*)/)[1];
  //   if (code) {
  //     this.setState({ status: STATUS.LOADING });
  //     fetch(`https://git-inspect-gatekeeper.herokuapp.com/authenticate/${code}`)
  //       .then(response => response.json())
  //       .then(({ token }) => {
  //         this.setState({
  //           token,
  //           status: STATUS.FINISHED_LOADING,
  //         });
  //       });
  //   }
  }

  // componentDidUpdate() {
  //   const REGISTER_URI = () => 'http://localhost:8000/register/';

  //   if (this.state.status === STATUS.FINISHED_LOADING) {
  //     axios.post(REGISTER_URI(), {
  //       headers: {
  //         Authorization: this.state.token,
  //       },
  //     })
  //       .then(response => response.json())
  //       .then(() => {
  //         this.setState({
  //           status: STATUS.AUTHENTICATED,
  //         });
  //       })
  //       .catch(() => {
  //         this.setState({
  //           token: null,
  //           status: STATUS.INITIAL,
  //         });
  //       });
  //   }
  // }

  render() {
    if (this.state.status === STATUS.INITIAL) {
      return <GithubLogin />;
    }
    if (this.state.status === STATUS.AUTHENTICATED) {
      return (
        <div className="ui segment">
          <div className="ui active inverted dimmer">
            <div className="ui text loader">Loading</div>
          </div>
          <p />
        </div>
      );
    }
    return <h3>{this.state.token}</h3>;
  }
}

export default hot(module)(Auth);
