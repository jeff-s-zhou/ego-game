/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from "react";
import {observer} from "mobx-react";
import {autorun, reaction, untracked} from "mobx";
import {target_types} from "./globals";
import {Enemy} from "./stores/combatants_store";


export const Targets = observer(({skills_store, combatants_store}) => {
    let t_types;
    if(skills_store.selected != null){
        t_types = skills_store.selected.valid_targets;
    }
    else {
        t_types = [target_types.single_enemy];
    }
    let targets = combatants_store.get_targets(t_types).map((target) => {
        return(<Target skills_store={skills_store}
                       target={target}
                       me={combatants_store.me}
                       key={target.id}/>)
    });

    return (
        <div>
        <h2>TARGETS</h2>
        <ul className="enemy-statuses">
        {targets}
        </ul>
        </div>
    )
});

const Target = observer(({target, me, skills_store}) =>  {
    function select_target(e) {
        if(target.selected) {
            if(me.up_to_bat){
                skills_store.cast(me, target);
            }
            else{
                let elem = document.getElementById("turn-fill");
                let id = setInterval(frame, 120);
                let flash_times = 7;
                function frame() {
                    if (flash_times <= 0) {
                        clearInterval(id);
                    } else {
                        flash_times--;
                        elem.style.width = (flash_times % 2 ? 0 : 100) + "%";
                    }
                }
            }
        }
        else {
            target.select();
        }
    }

    let css_class = target.selected ? "grey" : "";
    let name_style = target instanceof Enemy ? {color: '#cc00ff'} : {};

    return (
        <li className={css_class} onClick={select_target}>
            <span style={name_style}>{target.name}</span>
        </li>
    );
});