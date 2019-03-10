import React from 'react';
import axios from 'axios';
import _ from 'lodash';
import Commit from './Commit';

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
    this.loadCommits();
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

  loadCommits() {
    let promisse;
    const { next } = this.state;
    let { commits } = this.state;
    if (next != null) {
      promisse = axios.get(next);
    } else {
      promisse = axios.get('/commits/');
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
    if (commits.length === 0) {
      return null;
    }

    const elements = [];

    commits.forEach((element) => {
      elements.push(<Commit key={element.sha} data={element} />);
    });

    return (
      <div className="ui container segment">
        <div className="ui relaxed divided list">
          {elements}
          {isLoading && (
            <div className="item">
              <div className="content">
                <div className="ui active centered inline loader" />
              </div>
            </div>
          )}
          {!isLoading && hasNext && (
            <div className="item">
              <div clasName="content">
                <i className="big angle double down centered inline icon" />
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }
}

export default CommitList;
