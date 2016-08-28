/**
 * Created by Jeffrey on 7/4/2016.
 */

import React from 'react'

import {observable} from "mobx";
import {observer} from "mobx-react";

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

    //TODO: get actual skill based on character id, and not spoofing
    loadSkillsFromServer() {
        JQuery.ajax({
            url: ("/api/skill"),
            contentType: "application/json",
            dataType: "json",
            cache: false,
            success: (data) => {
                var my_skills = {};
                data.objects.map((skill) => {
                    my_skills[skill.id] = skill
                });
                app_state.skills = my_skills;
            },
            error: (xhr, status, err) => {
                console.error("api/ego", status, err.toString());
            }
        });
    }

    componentDidMount() {
        this.loadSkillsFromServer();

        socket.on('connect', () => {console.log("connected");});

        //chat
        socket.on('chat message', (msg) => {
            JQuery('#messages').append(JQuery('<li>').text(msg));
        });

        socket.on('current turn', (character_name) => {
            //console.log(character_name)
        });

        //state for just the character
        socket.on('my combat state', (my_combat_state) => {
            //this.setState({character_state:my_combat_state});
            app_state.character_state = my_combat_state;

            var old_skills = app_state.skills;
            my_combat_state.active_skills.map((skill) => {
                old_skills[skill.id].cooldown = skill.cooldown
            });
            //this.setState({skills: old_skills});
            app_state.skills = old_skills;
        });

        //state for my team
        socket.on('allies state', (allies_state) => {
            //this.setState({allies_state:allies_state});
            app_state.allies_state = allies_state;
        });

        //state for enemies
        socket.on('enemies state', (enemies_state) => {
            //this.setState({enemies_state:enemies_state});
            app_state.enemies_state = enemies_state;
        });
    }

    //<Allies my_state={this.state.character_state} allies_state={this.state.allies_state}/>

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