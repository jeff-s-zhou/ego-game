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
                <ul>
                {entries}
                </ul>
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
        var payload_updates = "";
        for(var key in this.props.entry.payloads_and_post_reactions){
            payload_updates = payload_updates + " " + key;
        }
        entry = this.props.entry.skill_cast + payload_updates;
    }
        return(
            <li>
                {entry}
            </li>
        )
    }
}

module.exports = CombatLog;