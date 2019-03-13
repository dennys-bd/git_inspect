import React from 'react';
import PropTypes from 'prop-types';

import CommitList from './CommitList';

const Repository = (props) => {
  const {
    match: {
      params: {
        id,
      },
    },
  } = props;

  // TODO: put a sub header with repository informations
  return <CommitList id={id} />;
};

Repository.propTypes = {
  match: PropTypes.shape({
    params: PropTypes.shape({
      id: PropTypes.string.isRequired,
    }).isRequired,
  }).isRequired,
};

export default Repository;
