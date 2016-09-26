/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from "react";
import {observer} from "mobx-react";
import {autorun, reaction, untracked} from "mobx";
import {Enemy} from "./stores/enemies_store";


export const Targets = observer(({actions_store, allies_store}) => {
    let targets = actions_store.targets;

    let target_components = targets.map((target) => {
        return(<Target actions_store={actions_store}
                       target={target}
                       me={allies_store.me}
                       key={target.id}/>)
    });

    return (
        <div>
        <h2>TARGETS</h2>
        <ul>{target_components}</ul>
        </div>
    )
});


const Target = observer(({target, me, actions_store}) =>  {
    //todo: abstract this out
    function select_target(e) {
        if(target.is_selected) {
            if(me.up_to_bat){
                actions_store.cast(me, target);
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

    let css_class = target.is_selected ? "grey" : "";
    let name_style = target instanceof Enemy ? {color: '#cc00ff'} : {};

    return (
        <li className={css_class} onClick={select_target}>
            <span style={name_style}>{target.name}</span>
        </li>
    );
});