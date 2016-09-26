/**
 * Created by Jeffrey on 7/4/2016.
 */

let React = require('react');
let ReactDOM = require('react-dom');
let Router = require('react-router/lib/Router');
let Route = require('react-router/lib/Route');
let IndexRoute = require('react-router/lib/IndexRoute');
let Link = require('react-router/lib/Link');

let BrowserHistory = require('react-router/lib/browserHistory');

//react bootstrap
let Grid = require('react-bootstrap/lib/Grid');

//react router-bootstrap
let LinkContainer = require('react-router-bootstrap/lib/LinkContainer');

//our own react modules, handled differently

import {AdventureContainer} from './adventure_container'

class App extends React.Component{
  render() {
    return (
      <Grid fluid>
                {this.props.children}
      </Grid>
    );
  }
}

ReactDOM.render((
  <Router history={BrowserHistory}>
      <Route path="/" component={App}>
          <IndexRoute component={AdventureContainer} />
      </Route>
  </Router>
  ), document.getElementById('content')
);

