/**
 * Created by Jeffrey on 7/4/2016.
 */

import React from 'react'

import {observable} from "mobx";
import {observer} from "mobx-react";
import {SkillsStore} from "./stores/my_skills_store";
import {TransportLayer} from "./transport_layer";
import {CombatantsStore} from "./stores/combatants_store";
import {CombatLogStore} from "./stores/combat_log_store";


var JQuery = require('jquery');
var Grid = require('react-bootstrap/lib/Grid');
var Row = require('react-bootstrap/lib/Row');
var Col = require('react-bootstrap/lib/Col');

var Skills = require('./skills');
var Allies = require('./allies');
var Targets = require('./targets');
var CombatLog = require('./combat_log');
var TurnBar = require('./turn_bar');
var TurnOrder = require('./turn_order');

var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

var transport_layer = new TransportLayer(socket);
var my_skills_store = new SkillsStore(transport_layer);
var combatants_store = new CombatantsStore(transport_layer);
var log_store = new CombatLogStore(transport_layer);


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
        <Row>
            <Col lg={2}>
                <Allies combatants_store={combatants_store}/>
            </Col>
            <Col lg={7}>
                <Row id="display" className="grey">
                    <Col lg={9}>
                        <CombatLog log_store={log_store}/>
                    </Col>
                    <Col lg={3}>
                        <TurnOrder combatants_store={combatants_store}/>
                    </Col>
                </Row>
                <Row>
                    <Col lg={12}>
                        <TurnBar combatants_store={combatants_store} />
                    </Col>
                </Row>
                <Row>
                    <Col lg={8}>
                        <Skills skills_store={my_skills_store}/>
                    </Col>
                    <Col lg={4}>
                        <Targets combatants_store={combatants_store}
                                 skills_store={my_skills_store}
                        />
                    </Col>
                </Row>
            </Col>
            <Col lg={3}>
                <ChatForm />
            </Col>
            </Row>
    )
  }
}

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