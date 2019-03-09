import React from 'react';
import axios from 'axios';
import Commit from './Commit';

class CommitList extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      commits: null,
    };
  }

  componentDidMount() {
    axios.get('/commits')
      .then((response) => {
        this.setState({ commits: response.data });
      })
      .catch((error) => {
        console.log('error: ', error);
      });
  }

  render() {
    const { commits } = this.state;
    if (commits == null) {
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
        </div>
      </div>
    );
  }
}

export default CommitList;
