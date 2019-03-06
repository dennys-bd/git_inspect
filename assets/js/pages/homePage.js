import React from 'react';
import ReactDOM from 'react-dom';
import RootApp from '../app/root-app';

const elem = document.getElementById('root-app');

if (elem != null) {
  ReactDOM.render(<RootApp />, document.getElementById('root-app'));
}
