/**
 * Created by Jeffrey on 8/26/2016.
 */

import React from "react";
import {observer} from "mobx-react";
import {Bar} from "./bar.js";


export const Allies = observer(({combatants_store}) => {
    let allies= combatants_store.ally_ids.map((ally_id) => {
        return(<Ally ally={combatants_store.allies[ally_id]} key={ally_id} />)
    });
    let me;
    if(combatants_store.me != null) {
        me = <Ally ally={combatants_store.me}/>
    }

    return (
    <div>
       <h2>TEAM</h2>
       <ul>
           {me}
           {allies}
       </ul>
    </div>
    )
});



const Ally = observer(({ally}) => {
    let width = Math.round((ally.hp/ally.max_hp) * 100);
    return (
        <li>
            {ally.name}
            < br />
            <Bar width={width} text={[ally.hp, "/", ally.max_hp]}/>
        </li>
    )
});