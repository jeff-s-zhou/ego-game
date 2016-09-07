/**
 * Created by Jeffrey on 9/4/2016.
 */


import React from 'react'
import {observer, action} from "mobx-react";

@observer
class CombatLog extends React.Component {
    render() {
    var entries = this.props.log_store.turn_entries.map((entry) => {
        return(
            <TurnEntry entry={entry} key={entry.id}/>
        )
    });

        return(
            <div id="combat-log">
                <h2>Combat</h2>
                <li>
                {entries}
                </li>
            </div>
        )
    }
}

@observer
class TurnEntry extends React.Component {
    render() {
    var entry;
    if(this.props.entry.skill_cast == ""){
        entry = "Turn has been skipped"
    }
    else{
        entry = this.props.entry.skill_cast
    }
        return(
            <ul>
                {entry}
            </ul>
        )
    }
}

module.exports = CombatLog;