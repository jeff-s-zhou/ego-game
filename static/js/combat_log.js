/**
 * Created by Jeffrey on 9/4/2016.
 */


import React from 'react'
import {observer, action} from "mobx-react";

@observer
class CombatLog extends React.Component {
    render() {
    var tabs = this.props.log_store.rounds.map((round) => {
        return <Tab item={round}/>
    });
    var tab_contents = this.props.log_store.rounds.map((round) => {
        return <TabContent item={round}/>
    });

    return(
        <div id="combat-log">
            <h2>COMBAT</h2>
            <ul className="tabs">
                {tabs}
            </ul>
            {tab_contents}
        </div>
    )
    }
}

//have to have own select function because of fucking javascript this contexts
@observer
class Tab extends React.Component {
    select() {
        this.props.item.select();
    }

    render() {
        var class_name = this.props.item.selected ? "tablinks active" : "tablinks";
        return (
            <li><a href="#" className={class_name} onClick={this.select.bind(this)}>{this.props.item.name}</a></li>
        )
    }
}

//TODO: generalize this later
const TabContent = observer(props => {
    var tab_visible_style = {
      display: props.item.selected ? "block" : "none"
    };

    var entries = props.item.turn_entries.map((entry) => {
        return(
            <TurnEntry entry={entry} key={entry.id}/>
        )
    });

    return (
        <div className="tabcontent" style={tab_visible_style}>
            <ul id="log-entries">
                {entries}
            </ul>
        </div>
    )
});


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
            payload_updates = payload_updates + key;
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