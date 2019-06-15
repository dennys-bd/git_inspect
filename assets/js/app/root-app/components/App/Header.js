import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import { Redirect, Link, Switch } from 'react-router-dom';
import SearchBar from './SearchBar';

class Header extends React.Component {
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
    axios.post('/api/repositories/?format=json', {
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
    let home = true;

    if (repo != null) {
      if (window.location.pathname !== '/commits') {
        return <Switch><Redirect to="/commits" /></Switch>;
      }
      return <Switch><Redirect to="/mycommits" /></Switch>;
    }

    if (window.location.pathname !== '/') {
      home = false;
    }

    return (
      <div>
        {!home && (
          <div className="ui breadcrumb">
            <i className="left angle icon divider" />
            <Link to="/">
              <div className="section">Home</div>
            </Link>
          </div>
        )}
        <div className="ui one column stackable center aligned page grid spacing">
          <div className="column twelve wide">
            <SearchBar key={key} text={text} onSubmit={t => this.onSearchSubmit(t)} title="Add a Repository" error={error} />
            {children}
          </div>
        </div>
      </div>
    );
  }
}

Header.defaultProps = {
  children: null,
};

Header.propTypes = {
  children: PropTypes.node,
};

export default Header;
