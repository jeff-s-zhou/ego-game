/**
 * Created by Jeffrey on 8/29/2016.
 */

import {observable, autorun, action} from "mobx";


export class MyCharacterStore {
    @observable name;
    @observable id;
    @observable hp;
    @observable mana;
    @observable active_skills_store;
    @observable statuses;

    constructor(transport_layer, active_skills_store) {
        this.transport_layer = transport_layer;
        this.transport_layer.update_my_combat_state = ((combat_state) => this.update_my_character(combat_state));
        this.name = "";
        this.id = 0;
        this.hp = 0;
        this.mana = 0;
        this.active_skills_store = active_skills_store;
        this.statuses = [];
        this.disposer = autorun(() => console.log("my hp is now " + this.hp));
        this.transport_layer.fetch_my_character();
    }

    update_my_character(state) {
        if (this.id === 0) {
            this.name = state.name;
            this.id = state.id;
            this.hp = state.hp;
            this.mana = state.mana;
            this.active_skills_store.load_skills(state.active_skills_store);
            //TODO: statuses
        }
        else {
            this.hp = state.hp;
            this.mana = state.mana;
            this.active_skills_store.update_skills(state.active_skills_store);
            //TODO: statuses
        }
    }
    //cast the currently selected skill on the ID
    @action cast_selected_on(target_id) {
        this.transport_layer.handle_input(this.id, this.active_skills_store.selected.id, target_id);
        //TODO: this might not actually be threadsafe
        this.active_skills_store.selected = null;
    }


}