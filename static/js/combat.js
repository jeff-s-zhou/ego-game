/**
 * Created by Jeffrey on 7/4/2016.
 */

import React from 'react'

import {observable} from "mobx";
import {observer} from "mobx-react";
import {MyCharacterStore} from "./stores/my_character_store";
import {SkillsStore} from "./stores/my_skills_store";
import {AlliesStore} from "./stores/allies_store";
import {EnemiesStore} from "./stores/enemies_store";
import {TransportLayer} from "./transport_layer";
import {CombatantsStore} from "./stores/combatants_store";


var JQuery = require('jquery');
var Grid = require('react-bootstrap/lib/Grid');
var Row = require('react-bootstrap/lib/Row');
var Col = require('react-bootstrap/lib/Col');

var Skills = require('./skills');
var Allies = require('./allies');
var Targets = require('./targets');

var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

var transport_layer = new TransportLayer(socket);
var my_skills_store = new SkillsStore(transport_layer);
var my_character_store = new MyCharacterStore(transport_layer, my_skills_store);
var allies_store = new AlliesStore(transport_layer);
var enemies_store = new EnemiesStore(transport_layer);
var combatants_store = new CombatantsStore(transport_layer, allies_store, enemies_store);



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
                    <Allies my_character_store = {my_character_store} allies_store = {allies_store}/>
                </Col>
                <Col lg={7}>
                    <Row>
                        <Col lg={12}>
                            <Display />
                        </Col>
                    </Row>
                    <Row>
                        <Col lg={8}>
                            <Skills skills_store={my_skills_store}/>
                        </Col>
                        <Col lg={4}>
                            <Targets combatants_store={combatants_store}/>
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