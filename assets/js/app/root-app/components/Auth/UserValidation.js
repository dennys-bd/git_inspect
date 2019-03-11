import React from 'react';
import lifecycle from 'react-pure-lifecycle';

const axios = require('axios');

const UserValidation = () => (
  <div className="ui segment padder">
    <div className="ui active inverted dimmer">
      <div className="ui text loader">Verifing your credentials...</div>
    </div>
    <p />
  </div>
);

const logout = () => {
  localStorage.clear();
  window.location.replace('/login');
};

const methods = {
  componentDidMount(props) {
    const { token, authenticate } = props;

    axios.get(`/verifytoken?token=${token}`)
      .then((response) => {
        if (response.status === 204) {
          authenticate();
        } else {
          logout();
        }
      })
      .catch(() => {
        logout();
      });
  },
};

export default lifecycle(methods)(UserValidation);
