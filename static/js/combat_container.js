/**
 * Created by Jeffrey on 9/24/2016.
 */
import React from "react";
import {Grid, Row, Col} from 'react-bootstrap';

import {observer} from "mobx-react";

import {SkillsStore} from "./stores/my_skills_store";
import {CombatantsStore} from "./stores/combatants_store";
import {CombatLogStore} from "./stores/combat_log_store";
import {EnemiesStore} from "./stores/enemies_store";

import {TurnOrder} from './turn_order';
import {TurnBar} from './turn_bar';

import {CombatDisplay} from './combat_display';
import {Actions} from './actions';
import {Targets} from './targets';

import {CombatTransportLayer} from './combat_transport_layer'

export class CombatContainer extends React.Component {
    constructor(props) {
        super(props);
        let combat_transport_layer = new CombatTransportLayer(props.socket);
        let enemies_store = new EnemiesStore(combat_transport_layer);
        let combatants_store = new CombatantsStore(combat_transport_layer, props.allies_store, enemies_store);
        this.state = {
            enemies_store: enemies_store,
            combatants_store: combatants_store,
            my_skills_store: new SkillsStore(combat_transport_layer, combatants_store),
            log_store: new CombatLogStore(combat_transport_layer)
        };
        combat_transport_layer.ready()
    }

    render() {
        return(
            <div>
                <Display
                    log_store={this.state.log_store}
                    enemies_store={this.state.enemies_store}
                    combatants_store={this.state.combatants_store}
                />
                <Row>
                    <Col lg={12}>
                        <TurnBar allies_store={this.props.allies_store} />
                    </Col>
                </Row>
                <ActionBar actions_store={this.state.my_skills_store} allies_store={this.props.allies_store}/>
            </div>
        )
    }
}


const Display = (({log_store, enemies_store, combatants_store}) => {
    return(
        <Row id="display" className="grey">
            <Col lg={9}>
                <CombatDisplay log_store={log_store} enemies_store={enemies_store}/>
            </Col>
            <Col lg={3}>
                <TurnOrder combatants_store={combatants_store}/>
            </Col>
        </Row>
    )
});

const ActionBar = ({actions_store, allies_store}) => {
    return(
        <Row>
            <Col lg={8}>
                <Actions actions_store={actions_store}/>
            </Col>
            <Col lg={4}>
                <Targets actions_store={actions_store} allies_store={allies_store}/>
            </Col>
        </Row>
    )
};
