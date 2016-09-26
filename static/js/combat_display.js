/**
 * Created by Jeffrey on 9/17/2016.
 */

import React from "react";
import {observer} from "mobx-react";
import {Bar} from "./bar.js";

export const CombatDisplay = observer(({log_store, enemies_store}) => {
    let entry = "";
    let round_index = "";
    if(log_store.current_turn != null) {
        if(log_store.current_turn.skill_cast == ""){
            entry = "Turn has been skipped";
            round_index = log_store.current_turn.round_index;
        }
        else{
            let payload_updates = "";
            let post_reaction_update = "";
            for(let key in log_store.current_turn.payloads_and_post_reactions){
                payload_updates = payload_updates + key;
                post_reaction_update = log_store.current_turn.payloads_and_post_reactions[key]
            }
            entry = log_store.current_turn.skill_cast + payload_updates + post_reaction_update;
            enemies_store.enemy_ids.map((enemy_id) => {
                let enemy_name = enemies_store.enemies[enemy_id].name;
                entry = entry.replace(new RegExp(enemy_name, 'g'),
                    '<span style="color: #cc00ff;">' + enemy_name + '</span>');
            });
        }
    }

    let enemies = enemies_store.enemy_ids.map((enemy_id) => {
            return(<EnemyStatus enemy={enemies_store.enemies[enemy_id]} key={enemy_id}/>)
    });

    return (
        <div>
            <h2>{"COMBAT / ROUND / TURN " + round_index}</h2>
            <ul>
                <li>
                    <div dangerouslySetInnerHTML={{__html: entry}} />
                </li>
            </ul>
            <ul className="enemy-statuses">
            {enemies}
            </ul>
        </div>
    );
});


const EnemyStatus = observer(({enemy}) => {
    let width = Math.round((enemy.hp/enemy.max_hp) * 100);
    return (
        <li>
            {enemy.name}
            < br />
            <Bar width={width} text={""}/>
        </li>
    )
});