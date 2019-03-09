import React from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import Status from './Status';

class CheckCommits extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      status: Status.INITIAL,
    };
  }

  componentDidMount() {
    axios.get('/checkcommits')
      .then(() => {
        this.setState({ status: Status.HAS_COMMIT });
      })
      .catch(() => {
        this.setState({ status: Status.HASNT_COMMIT });
      });
  }

  render() {
    const { status } = this.state;
    if (status === Status.INITIAL) {
      return (
        <div className="center">
          <div className="ui active inverted dimmer">
            <div className="ui text loader">Verifing your commits...</div>
          </div>
          <p />
        </div>
      );
    }
    if (status === Status.HAS_COMMIT) {
      return (
        <div className="center">
          <div className="ui horizontal divider">
            Or
          </div>
          <Link to="/commits">
            <div className="ui right labeled icon basic button">
              Go to your Commits
              <i className="github icon" />
            </div>
          </Link>
        </div>
      );
    }
    return null;
  }
}

export default CheckCommits;
