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
            <h2>TURN ORDER</h2>
            <ul>
                {combatant_elements}
            </ul>
        </div>
    )
});

const Combatant = observer((props) => {
    var up_to_bat = props.combatant.up_to_bat ? "turn-indicator" : "not-turn";
    return (
        <li><div className={up_to_bat}></div>{props.combatant.name} </li>
    )
});

module.exports = TurnBar;