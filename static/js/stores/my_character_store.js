/**
 * Created by Jeffrey on 8/29/2016.
 */

import {observable, autorun, action} from "mobx";


export class MyCharacterStore {
    @observable name;
    @observable id;
    @observable hp;
    @observable mana;
    @observable active_skills;
    @observable statuses;

    constructor(transport_layer, active_skills) {
        this.transport_layer = transport_layer;
        this.transport_layer.update_my_combat_state = ((combat_state) => this.update_my_character(combat_state));
        this.name = "";
        this.id = 0;
        this.hp = 0;
        this.mana = 0;
        this.active_skills = active_skills;
        this.statuses = [];
        this.disposer = autorun(() => console.log("my hp is now " + this.hp));
        this.transport_layer.fetch_my_character();
    }

    update_my_character(state) {
        if(this.id === 0) {
            this.name = state.name;
            this.id = state.id;
            this.hp = state.hp;
            this.mana = state.mana;
            this.active_skills.load_skills(state.active_skills);
            //TODO: statuses
        }
        else {
            console.log("calling update my character");
            this.hp = state.hp;
            this.mana = state.mana;
            this.active_skills.update_skills(state.active_skills);
            //TODO: statuses
        }


    }
}