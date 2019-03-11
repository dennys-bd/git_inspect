import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import { Redirect, Switch } from 'react-router-dom';
import SearchBar from './SearchBar';

class AddARepo extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      error: null,
      repo: null,
      text: '',
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

    const { children } = this.props;

    if (repo != null) {
      return <Switch><Redirect to="/commits" /></Switch>;
    }

    return (
      <div className="ui container center aligned">
        <SearchBar key={key} text={text} onSubmit={t => this.onSearchSubmit(t)} title="Add a Repository" error={error} />
        {children}
      </div>
    );
  }
}

AddARepo.defaultProps = {
  children: null,
};

AddARepo.propTypes = {
  children: PropTypes.node,
};

export default AddARepo;
