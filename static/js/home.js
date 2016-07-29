/**
 * Created by Jeffrey on 7/4/2016.
 */

var React = require('react');
var JQuery = require('jquery');
var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port);
socket.on('connect', function(){console.log("connected");});
socket.on('event', function(data){});
socket.on('disconnect', function(){});

module.exports = Home = React.createClass({
    loadPlayersFromServer: function(playerId) {
        JQuery.ajax({
            url: ("/api/player/" + playerId),
            contentType: "application/json",
            dataType: "json",
            cache: false,
            success: function(data) {
                this.setState({hp: data.hp});
            }.bind(this),
            error: function(xhr, status, err) {
                console.error("api/ego", status, err.toString());
            }.bind(this)
        });
    },

    //loadFightFromServer

    componentDidMount(){
        this.loadPlayersFromServer(1);
    },

    getInitialState() {
        return {}
    },

    render: function() {
    return (
        <div className="Home">
        <ul id="messages"></ul>
        <form action="">
          <input id="m" autocomplete="off" /><button>Send</button>
        </form>
        </div>
    );
  }
});