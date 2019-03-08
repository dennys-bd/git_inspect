import React from 'react';
import PropsTypes from 'prop-types';

class SearchBar extends React.Component {
  constructor(props) {
    super(props);

    const { title } = this.props;

    this.state = {
      text: '',
      title,
    };
  }

  onFormSubmit(e) {
    e.preventDefault();

    const { text } = this.state;
    const { onSubmit } = this.props;

    onSubmit(text);
  }

  // TODO: ERROR AND LOADING TREATEMENTS
  render() {
    const { text, title } = this.state;

    return (
      <div className="ui segment">
        <form onSubmit={e => this.onFormSubmit(e)} className="ui form">
          <div className="field">
            <h3>{title}</h3>
            <input
              type="text"
              text={text}
              onChange={e => this.setState({ text: e.target.value })}
            />
          </div>
        </form>
      </div>
    );
  }
}

SearchBar.defaultProps = {
  onSubmit: () => {},
  title: '',
};

SearchBar.propTypes = {
  onSubmit: PropsTypes.func,
  title: PropsTypes.string,
};

export default SearchBar;
