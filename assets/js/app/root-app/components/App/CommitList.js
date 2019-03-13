import React from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import _ from 'lodash';

import Commit from './Commit';
import Header from './Header';

class CommitList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      error: false,
      hasNext: true,
      next: null,
      isLoading: true,
      commits: [],
    };

    this.onScroll = this.onScroll.bind(this);
    this.loadCommits = this.loadCommits.bind(this);
  }

  componentDidMount() {
    // TODO: call loadCommits again if screen is not completed filled yet
    const { id } = this.props;
    this.loadCommits(id);
    const debounced = _.debounce(this.onScroll, 50);
    window.addEventListener('scroll', _.debounce(debounced));
  }

  componentWillUnmount() {
    window.removeEventListener('scroll', this.onScroll);
  }

  onScroll() {
    const {
      loadCommits,
      state: {
        error,
        isLoading,
        hasNext,
      },
    } = this;

    if (error || isLoading || !hasNext) return;

    if ((window.innerHeight + window.scrollY) >= (document.body.scrollHeight - 100)) {
      this.setState({ isLoading: true }, loadCommits());
    }
  }

  loadCommits(id) {
    let promisse;
    const { next } = this.state;
    let { commits } = this.state;
    if (next != null) {
      promisse = axios.get(next);
    } else if (id == null) {
      promisse = axios.get('/commits/');
    } else {
      promisse = axios.get(`/commits/?repository__id=${id}`);
    }
    promisse
      .then((response) => {
        commits = commits.concat(response.data.results);
        const hasNext = response.data.next != null;
        this.setState({
          commits,
          hasNext,
          next: response.data.next,
          isLoading: false,
        });
      })
      .catch(() => {
        this.setState({
          hasNext: false,
          isLoading: false,
          error: true,
        });
      });
  }


  render() {
    const { hasNext, commits, isLoading } = this.state;

    if (commits.length === 0 && !hasNext) {
      return (
        <Header>
          <div className="ui message">
            <div className="header">
              Added successfully, your repository is tracked now.
            </div>
            <ul className="list">
              <li>It appears that you have not committed in it for the last 30 days</li>
              <li>
                Don not worry once you push something to your repository we will receive it too.
              </li>
              <li>You do not have to add this repository again.</li>
            </ul>
          </div>
        </Header>
      );
    }
    if (commits.length === 0) {
      return null;
    }

    const elements = [];

    commits.forEach((element) => {
      elements.push(<Commit key={element.sha} data={element} />);
    });

    return (
      <Header>
        <div className="ui segment">
          <div className="ui relaxed divided list">
            {elements}
            {isLoading && (
              <div className="item">
                <div className="content center aligned">
                  <div className="ui active inline loader" />
                </div>
              </div>
            )}
            {!isLoading && hasNext && (
              <div className="item">
                <div className="content">
                  <i className="big angle double down inline icon" />
                </div>
              </div>
            )}
          </div>
        </div>
      </Header>
    );
  }
}

CommitList.defaultProps = {
  id: null,
};

CommitList.propTypes = {
  id: PropTypes.string,
};

export default CommitList;
