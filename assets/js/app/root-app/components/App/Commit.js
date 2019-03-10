import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';

const Commit = (props) => {
  const { data } = props;

  const timeSince = (date) => {
    const seconds = Math.floor((new Date() - date) / 1000);
    let interval = Math.floor(seconds / 31536000);

    if (interval > 1) {
      return `${interval} years`;
    }
    interval = Math.floor(seconds / 2592000);
    if (interval > 1) {
      return `${interval} months`;
    }
    interval = Math.floor(seconds / 86400);
    if (interval > 1) {
      return `${interval} days`;
    }
    interval = Math.floor(seconds / 3600);
    if (interval > 1) {
      return `${interval} hours`;
    }
    interval = Math.floor(seconds / 60);
    if (interval > 1) {
      return `${interval} minutes`;
    }
    return `${Math.floor(seconds)} seconds`;
  };

  return (
    <div className="item">
      <i className="large github middle aligned icon" />
      <div className="content">
        <a className="header" href={data.url}>{data.message}</a>
        <Link to={`repository/${data.repository_id}`}>{data.repository_name}</Link>
        <div className="description">
          {`${timeSince(Date.parse(data.created))} ago`}
        </div>
      </div>
    </div>
  );
};

Commit.defaultProps = {
  data: {},
};

Commit.propTypes = {
  data: PropTypes.shape({
    sha: PropTypes.string,
    url: PropTypes.string,
    author: PropTypes.shape({
      date: PropTypes.string,
      name: PropTypes.string,
      email: PropTypes.string,
    }),
    message: PropTypes.string,
    created: PropTypes.string,
    repository_name: PropTypes.string,
    repository_id: PropTypes.number,
  }),
};

export default Commit;
