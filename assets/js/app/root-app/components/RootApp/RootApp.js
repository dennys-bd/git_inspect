import React from 'react';
import SearchBar from '../SearchBar/SearchBar';

class RootApp extends React.Component {
  // onSearchSubmit(text) {
  //   console.log(text);
  // }

  render() {
    return (
      <div className="ui container" style={{ marginTop: '10px' }}>
        <SearchBar onSubmit={this.onSearchSubmit} title="Add a Repository" />
      </div>
    );
  }
}

export default RootApp;
