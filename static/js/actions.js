/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from "react";
import {observer, action} from "mobx-react";
import {autorun, reaction, untracked} from "mobx";


export const Actions = observer(({actions_store}) => {
    let my_actions = actions_store.action_ids.map((action_id) => {
        let action = actions_store.actions[action_id];
        return (<Action key={action_id} action={action}/>)
    });

    return (
        <div>
            <h2>Actions</h2>
            <ul>
            {my_actions}
            </ul>
        </div>
    );
});

const Action = observer(({action}) => {
    function select_action(e) {
        action.select();
    }
    let css_class = action.is_selected ? "grey" : "";
    let action_component;
    if(action.valid) {
        action_component = <div className={css_class} onClick={select_action}>{action.text}</div>
    }
    else {
        action_component = <div className="greyed-text">{action.text}</div>
    }

    return (
        <li>
            {action_component}
        </li>
    )
});

