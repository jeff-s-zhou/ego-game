/**
 * Created by Jeffrey on 7/4/2016.
 */

import React from 'react'

import {observable} from "mobx";
import {observer} from "mobx-react";
import {MyCharacterStore, MySkillsStore, TargetsStore} from "stores";
import {TransportLayer} from "transport_layer";

var JQuery = require('jquery');
var Grid = require('react-bootstrap/lib/Grid');
var Row = require('react-bootstrap/lib/Row');
var Col = require('react-bootstrap/lib/Col');

var Skills = require('./skills');
var Allies = require('./allies');
var Targets = require('./targets');

var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

var app_state = observable({
    character_state:{name:'', id:0, hp:0, mana:0, active_skills:[], statuses:[]},
    allies_state:[],
    enemies_state:[],
    messages:[],
    skills:{}
});


@observer
class Home extends React.Component{
    constructor(props) {
        super(props);
    }


    componentDidMount() {
        //chat
        socket.on('chat message', (msg) => {
            JQuery('#messages').append(JQuery('<li>').text(msg));
        });
    }
    render() {
    return (
        <Grid>
            <Row>
                <Col lg={2}>

                </Col>
                <Col lg={7}>
                    <Row>
                        <Col lg={12}>
                            <Display />
                        </Col>
                    </Row>
                    <Row>
                        <Col lg={8}>
                            <Skills app_state={app_state}/>
                        </Col>
                        <Col lg={4}>
                            {//<Targets enemies_state={this.state.enemies_state}/>
                            }
                        </Col>
                    </Row>
                </Col>
                <Col lg={3}>
                    <ChatForm />
                </Col>
            </Row>
        </Grid>
    )
  }
}

@observer
class Display extends React.Component{
    render() {
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
}

@observer
class ChatForm extends React.Component {
    handleSubmit(e) {
        console.log("handling Submit");
        socket.emit('chat message', JQuery('#m').val());
        JQuery('#m').val('');
    }
    render() {
        return (
        <div className="Home">
        <ul id="messages"></ul>
        <form action="" onSubmit={this.handleSubmit}>
          <input id="m" autoComplete="off" /><button>Send</button>
        </form>
        </div>
        );
    }
}

module.exports = Home;