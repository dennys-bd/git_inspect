import React from 'react';
import { hot } from 'react-hot-loader';
import STATUS from './status';
import GithubLogin from './GithubLogin';
import App from '../App/App';

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
    if (this.state.status === STATUS.AUTHENTICATED) {
      return <App />;
    }
    return <GithubLogin />;
  }
}

export default hot(module)(Auth);

// if (this.state.status === STATUS.AUTHENTICATED) {
//   return (
//     <div className="ui segment">
//       <div className="ui active inverted dimmer">
//         <div className="ui text loader">Loading</div>
//       </div>
//       <p />
//     </div>
//   );
// }
