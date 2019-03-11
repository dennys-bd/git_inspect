import React from 'react';
import { hot } from 'react-hot-loader';
import {
  BrowserRouter, Switch, Route, Redirect,
} from 'react-router-dom';
import axios from 'axios';
import Auth from '../Auth/Auth';
import App from '../App/App';
import CommitList from '../App/CommitList';
import STATUS from '../Auth/Status';

import './style.scss';

class RootApp extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      user: STATUS.INITIAL,
    };

    this.authenticate = this.authenticate.bind(this);
  }

  authenticate() {
    axios.defaults.headers.common.Authorization = `Token ${localStorage.getItem('token')}`;
    this.setState({ user: STATUS.AUTHENTICATED });
  }

  render() {
    const { user } = this.state;

    // <Route path="/repository/:id" component={Repository} />;
    if (user === STATUS.AUTHENTICATED) {
      return (
        <BrowserRouter>
          <Switch>
            <Redirect from="/login" to="/" />
            <Route path="/" exact component={App} />
            <Route path="/commits" component={CommitList} />
          </Switch>
        </BrowserRouter>
      );
    }

    window.history.pushState({ urlPath: '/login' }, '', '/login');
    return <Auth authenticate={this.authenticate} />;
  }
}

export default hot(module)(RootApp);
