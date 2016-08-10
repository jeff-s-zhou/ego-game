/**
 * Created by Jeffrey on 7/4/2016.
 */

var React = require('react');
var JQuery = require('jquery');
var Grid = require('react-bootstrap/lib/Grid');
var Row = require('react-bootstrap/lib/Row');
var Col = require('react-bootstrap/lib/Col');

var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port);
socket.on('connect', function(){console.log("connected");});
socket.on('chat message', function(msg){
    JQuery('#messages').append(JQuery('<li>').text(msg));
});

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

    getInitialState() {
        return {}
    },

    render: function() {
    return (
        <Grid>
            <Row>
                <Col lg={2}>
                    <Status />
                </Col>
                <Col lg={7}>
                    <Row>
                        <Col lg={12}>
                            <Display />
                        </Col>
                    </Row>
                    <Row>
                        <Col lg={8}>
                            <Skills/>
                        </Col>
                        <Col lg={4}>
                            <Targets/>
                        </Col>
                    </Row>
                </Col>
                <Col lg={3}>
                    <ChatForm />
                </Col>
            </Row>
        </Grid>
    );
  }
});

var Status = React.createClass({
   render: function() {
       return (
           <div>
               <h1>Status</h1>
               <ul>
                   <li>Larken</li>
                   <li>Ilfantz</li>
                   <li>Vimilikirti</li>
               </ul>
           </div>
       )
   }
});

var Display = React.createClass({

    render: function() {
        return (
            <div id="combat">
                <h1>Combat</h1>
                <ul>
                    <li>Millia begins FOCUSING.</li>

                    <li>Khazarak uses MEZZO SLASH on Ilfantz, dealing 12 DAMAGE.</li>

                    <li>Ilfantz is heavily wounded!</li>

                    <li>Vimilikirti uses SHADOW STUTTER, dealing 15 DAMAGE to ALL ENEMIES!</li>

                    <li>Vimilikirti is now EVASIVE for 2 TURNS.</li>

                    <li>YOU are going!</li>

                    <li>NEXT: Ilfantz, Sinistr, Mazara, Verit</li>
                </ul>
            </div>
        );
    }
});

var Skills = React.createClass({
    render: function() {
        return (
            <h1>Skills</h1>
        );
    }
});

var Targets = React.createClass({
    render: function() {
        return (
            <h1>Targets</h1>
        );
    }
});

var ChatForm = React.createClass({
    handleSubmit: function(e) {
        console.log("handling Submit");
        socket.emit('chat message', JQuery('#m').val());
        JQuery('#m').val('');
    },
    render: function() {
        return (
        <div className="Home">
        <ul id="messages"></ul>
        <form action="" onSubmit={this.handleSubmit}>
          <input id="m" autoComplete="off" /><button>Send</button>
        </form>
        </div>
        );
    }
});