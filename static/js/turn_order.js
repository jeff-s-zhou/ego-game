/**
 * Created by Jeffrey on 9/6/2016.
 */

import React from 'react'
import {observer} from "mobx-react";

const TurnBar = observer((props) => {
    var combatants = props.combatants_store.combatant_ids.map((id) => {
        return props.combatants_store.combatants[id];
    });
    combatants.sort((a, b) => {
        return a.order - b.order;
    });
    var combatant_elements = combatants.map((combatant) => {
        return (
            <Combatant key={combatant.id} combatant={combatant}/>
        )
    });
    return (
        <div>
            <h2>Turn Order</h2>
            <ul>
                {combatant_elements}
            </ul>
        </div>
    )
});

const Combatant = observer((props) => {
    var up_to_bat = props.combatant.up_to_bat ? "!" : ".";
    return (
        <li>{props.combatant.name} {up_to_bat}</li>
    )
});

module.exports = TurnBar;