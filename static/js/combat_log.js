/**
 * Created by Jeffrey on 9/4/2016.
 */


import React from 'react'
import {observer, action} from "mobx-react";


@observer
class CombatLog extends React.Component {
    render() {
    let tabs = this.props.log_store.rounds.map((round) => {
        return <Tab item={round}/>
    });
    let tab_contents = this.props.log_store.rounds.map((round) => {
        return <TabContent item={round} combatants_store={this.props.combatants_store}/>
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
        let class_name = this.props.item.is_selected ? "tablinks active" : "tablinks";
        return (
            <li><a href="#" className={class_name} onClick={this.select.bind(this)}>{this.props.item.name}</a></li>
        )
    }
}

//TODO: generalize this later
const TabContent = observer(props => {
    let tab_visible_style = {
      display: props.item.is_selected ? "block" : "none"
    };

    let entries = props.item.turn_entries.map((entry) => {
        return(
            <TurnEntry entry={entry} combatants_store={props.combatants_store} key={entry.id}/>
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
    let entry;
    if(this.props.entry.skill_cast == ""){
        entry = "Turn has been skipped"
    }
    else{
        let payload_updates = "";
        let post_reaction_update = "";
        for(let key in this.props.entry.payloads_and_post_reactions){
            payload_updates = payload_updates + key;
            post_reaction_update = this.props.entry.payloads_and_post_reactions[key]
        }
        entry = this.props.entry.skill_cast + payload_updates + post_reaction_update;
        for(let i = 0; i < this.props.combatants_store.enemy_ids.length; i++) {
            let enemy_id = this.props.combatants_store.enemy_ids[i];
            let enemy_name = this.props.combatants_store.enemies[enemy_id].name;
            entry = entry.replace(new RegExp(enemy_name, 'g'),
                '<span style="color: #cc00ff;">' + enemy_name + '</span>');
        }

    }
        return(

            <li>
                <div dangerouslySetInnerHTML={{__html: entry}} />
            </li>
        )
    }
}

module.exports = CombatLog;