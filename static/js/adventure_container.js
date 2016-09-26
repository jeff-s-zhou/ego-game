/**
 * Created by Jeffrey on 7/4/2016.
 */

import React from "react";
import {JQuery} from 'jquery';
import {Grid, Row, Col} from 'react-bootstrap';

import {observer} from "mobx-react";

import {TransportLayer} from "./transport_layer";

import {ChatStore} from "./stores/chat_store";
import {AlliesStore} from "./stores/allies_store";
import {EVENT_TYPE, UIStore} from "./stores/ui_store";
import {Allies} from './allies';
import {Chat} from './chat';
import {CombatContainer} from './combat_container'
import {StaticEventContainer} from './static_event_container'


let socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

@observer
export class AdventureContainer extends React.Component {
    constructor(props) {
        super(props);
        let transport_layer = new TransportLayer(socket);
        let allies_store = new AlliesStore(transport_layer);
        this.state = {
            allies_store: allies_store,
            chat_store: new ChatStore(transport_layer),
            ui_store: new UIStore(transport_layer)
        };
        transport_layer.ready();
    }

    render() {
        return (
            <Row>
                <h1>test 6990</h1>
                <Sidebar allies_store={this.state.allies_store}/>
                <Event
                    ui_store={this.state.ui_store}
                    socket={socket}
                    allies_store = {this.state.allies_store}
                />
                <Col lg={3}>
                    <Chat chat_store={this.state.chat_store} allies_store={this.state.allies_store}/>
                </Col>
            </Row>
        )
    }
}

const Sidebar = (({allies_store}) => {
    return(
        <Col lg={2}>
            <Allies allies_store={allies_store}/>
        </Col>
    )
});

const Event = observer(({ui_store, socket, allies_store}) => {
    let get_event_container = (event_type) => {
        if (event_type == EVENT_TYPE.combat) {
            return <CombatContainer socket={socket} allies_store={allies_store}/>
        }
        else {
            return <StaticEventContainer allies_store={allies_store}/>
        }
    };
    return (
        <Col lg={7}>
            {get_event_container(ui_store.event_type)}
        </Col>
    )
});




