import React from 'react';
import { hot } from 'react-hot-loader';
import {
  BrowserRouter, Switch, Route, Redirect,
} from 'react-router-dom';
import Auth from '../Auth/Auth';
import App from '../App/App';
import STATUS from '../Auth/Status';

class RootApp extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      user: STATUS.INITIAL,
    };

    this.authenticate = this.authenticate.bind(this);
  }

  authenticate() {
    this.setState({ user: STATUS.AUTHENTICATED });
  }

  render() {
    const { user } = this.state;

    if (user === STATUS.AUTHENTICATED) {
      return (
        <BrowserRouter>
          <Switch>
            <Redirect from="/login" to="/" />
            <Route path="/" exact component={App} />
          </Switch>
        </BrowserRouter>
      );
    }

    window.history.pushState({ urlPath: '/login' }, '', '/login');
    return <Auth authenticate={this.authenticate} />;
  }
}

export default hot(module)(RootApp);
