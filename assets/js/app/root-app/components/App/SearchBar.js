import React from 'react';
import PropsTypes from 'prop-types';
import Status from './Status';

class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    const {
      text, title, error, status,
    } = this.props;

    this.state = {
      text,
      status,
      error,
      title,
    };
  }

  onFormSubmit(e) {
    e.preventDefault();

    const { text } = this.state;
    const { onSubmit } = this.props;

    this.setState({ status: Status.LOADING });
    onSubmit(text);
  }

  getForm(inside) {
    const { status, error } = this.state;
    if (status === Status.LOADING) {
      return (
        <form className="ui loading form">
          {inside}
        </form>
      );
    }
    if (error != null) {
      return (
        <form onSubmit={e => this.onFormSubmit(e)} className="ui form">
          {inside}
          <div className="ui error message">
            <div className="header">Action Forbidden</div>
            <p>
              {error}
              .
            </p>
          </div>
        </form>
      );
    }
    return (
      <form onSubmit={e => this.onFormSubmit(e)} className="ui form">
        {inside}
      </form>
    );
  }


  render() {
    const { text, title } = this.state;
    return (
      <div className="ui segment header">
        {this.getForm(
          <div className="field">
            <h3>{title}</h3>
            <input
              type="text"
              text={text}
              onChange={e => this.setState({ text: e.target.value })}
            />
          </div>,
        )}
      </div>
    );
  }
}

SearchBar.defaultProps = {
  onSubmit: () => {},
  text: '',
  error: null,
  title: 'Search',
  status: Status.INITIAL,
};

SearchBar.propTypes = {
  onSubmit: PropsTypes.func,
  title: PropsTypes.string,
  error: PropsTypes.string,
  status: PropsTypes.string,
  text: PropsTypes.string,
};

export default SearchBar;
