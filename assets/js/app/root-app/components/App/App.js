import React from 'react';
import axios from 'axios';
import SearchBar from './SearchBar';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      hasError: false,
      repo: null,
    };
  }

  onSearchSubmit(text) {
    axios.post('/repositories/?format=json', {
      name: text,
    })
      .then(() => {
        this.setState({ repo: text });
      })
      .catch(() => {
        this.setState({ hasError: true });
      });
  }

  render() {
    const { repo, hasError } = this.state;

    if (repo != null) {
      console.log('change page');
    }
    return (
      <div className="ui container" style={{ marginTop: '10px' }}>
        <SearchBar onSubmit={t => this.onSearchSubmit(t)} title="Add a Repository" has_error={hasError} />
      </div>
    );
  }
}

export default App;
