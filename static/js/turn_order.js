/**
 * Created by Jeffrey on 9/6/2016.
 */

import React from 'react'
import {observer} from "mobx-react";
import {Enemy} from "./stores/combatants_store";

export const TurnOrder = observer((props) => {
    let combatants = props.combatants_store.combatant_ids.map((id) => {
        return props.combatants_store.combatants[id];
    });
    combatants.sort((a, b) => {
        return a.order - b.order;
    });
    let combatant_components = combatants.map((combatant) => {
        return (
            <Combatant key={combatant.id} combatant={combatant}/>
        )
    });
    return (
        <div>
            <h2>TURN ORDER</h2>
            <ul>
                {combatant_components}
            </ul>
        </div>
    )
});


const Combatant = observer((props) => {
    let up_to_bat = props.combatant.up_to_bat ? "turn-indicator" : "not-turn";
    let name_style = props.combatant instanceof Enemy ? {color: '#cc00ff'} : {};
    return (
        <li><div className={up_to_bat}></div><span style={name_style}>{props.combatant.name}</span></li>
    )
});
