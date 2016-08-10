/**
 * Created by Jeffrey on 7/4/2016.
 */

var React = require('react');
var ReactDOM = require('react-dom');
var Router = require('react-router/lib/Router');
var Route = require('react-router/lib/Route');
var IndexRoute = require('react-router/lib/IndexRoute');
var Link = require('react-router/lib/Link');
var JQuery = require('jquery');

//react bootstrap
var Grid = require('react-bootstrap/lib/Grid');

//react router-bootstrap
var LinkContainer = require('react-router-bootstrap/lib/LinkContainer');

//our own react modules, handled differently

var Combat = require('./combat');

var App = React.createClass({
  render: function() {
    return (
      <Grid>
                {this.props.children}
      </Grid>
    );
  }
});

ReactDOM.render((
        <Router>
            <Route path="/" component={App}>
                <IndexRoute component={Combat} />
            </Route>
        </Router>
    ), document.getElementById('content')
);
