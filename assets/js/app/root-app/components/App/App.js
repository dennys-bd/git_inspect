import React from 'react';
import axios from 'axios';
import { Redirect, Switch } from 'react-router-dom';
import SearchBar from './SearchBar';
import CheckCommits from './CheckCommits';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hasError: false,
      repo: null,
    };
  }

  onSearchSubmit(text) {
    // TODO: LOADING ON SEARCH BAR
    axios.post('/repositories/?format=json', {
      name: text,
    })
      .then(() => {
        this.setState({ repo: text });
      })
      .catch(() => {
        // TODO: SHOW ERROR ON SEARCH BAR
        this.setState({ hasError: true });
      });
  }

  render() {
    const { repo, hasError } = this.state;

    if (repo != null) {
      return <Switch><Redirect to="/commits" /></Switch>;
    }

    return (
      <div className="outer">
        <div className="middle">
          <div className="ui container center" style={{ marginTop: '10px' }}>
            <SearchBar onSubmit={t => this.onSearchSubmit(t)} title="Add a Repository" has_error={hasError} />
          </div>
          <CheckCommits />
        </div>
      </div>
    );
  }
}

export default App;
