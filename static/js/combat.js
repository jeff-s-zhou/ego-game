/**
 * Created by Jeffrey on 7/4/2016.
 */

import React from "react";
import {JQuery} from 'jquery';
import {Grid, Row, Col} from 'react-bootstrap';

import {observable} from "mobx";
import {observer} from "mobx-react";

import {SkillsStore} from "./stores/my_skills_store";
import {TransportLayer} from "./transport_layer";
import {CombatantsStore} from "./stores/combatants_store";
import {CombatLogStore} from "./stores/combat_log_store";
import {ChatStore} from "./stores/chat_store";

import {TurnOrder} from './turn_order';
import {TurnBar} from './turn_bar';
import {Skills} from './skills';
import {Allies} from './allies';
import {Targets} from './targets';
import {CombatEvent} from './combat_event';
import {Chat} from './chat';


let socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

let transport_layer = new TransportLayer(socket);
let my_skills_store = new SkillsStore(transport_layer);
let combatants_store = new CombatantsStore(transport_layer);
let log_store = new CombatLogStore(transport_layer);
let chat_store = new ChatStore(transport_layer);



export const CombatContainer = ((props) => {
    return (
        <Row>
            <h1>test 160</h1>
            <Sidebar />
            <Col lg={7}>
                <Display />
                <Row>
                    <Col lg={12}>
                        <TurnBar combatants_store={combatants_store} />
                    </Col>
                </Row>
                <ActionBar />
            </Col>
            <Col lg={3}>
                <Chat chat_store={chat_store} combatants_store={combatants_store}/>
            </Col>
        </Row>
    )
});



const Sidebar = ((props) => {
    return(
        <Col lg={2}>
            <Allies combatants_store={combatants_store}/>
        </Col>
    )
});


const Display = ((props) => {
    return(
        <Row id="display" className="grey">
            <Col lg={9}>
                <CombatEvent log_store={log_store} combatants_store={combatants_store}/>
            </Col>
            <Col lg={3}>
                <TurnOrder combatants_store={combatants_store}/>
            </Col>
        </Row>
    )
});


const ActionBar = ((props) => {
    return(
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
    )
});

