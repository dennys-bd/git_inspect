import React from 'react';
import axios from 'axios';
import { Redirect, Switch } from 'react-router-dom';
import SearchBar from './SearchBar';
import CheckCommits from './CheckCommits';

import './style.scss';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      error: null,
      repo: null,
      text: '',
      key: 1,
    };
  }

  onSearchSubmit(text) {
    const { key } = this.state;
    axios.post('/repositories/?format=json', {
      name: text,
    })
      .then(() => {
        this.setState({ repo: text });
      })
      .catch((e) => {
        this.setState({ error: e.response.data.detail, key: key + 1, text });
      });
  }

  render() {
    const {
      text, key, repo, error,
    } = this.state;

    if (repo != null) {
      return <Switch><Redirect to="/commits" /></Switch>;
    }

    return (
      <div className="outer">
        <div className="middle">
          <div className="ui container center" style={{ marginTop: '10px' }}>
            <SearchBar key={key} text={text} onSubmit={t => this.onSearchSubmit(t)} title="Add a Repository" error={error} />
          </div>
          <CheckCommits />
        </div>
      </div>
    );
  }
}

export default App;
