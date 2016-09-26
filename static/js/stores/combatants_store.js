/**
 * Created by Jeffrey on 8/29/2016.
 */


import {observable, autorun, action, computed, reaction} from "mobx";

export class CombatantsStore {
    allies_store;
    enemies_store;
    @observable current_combatant;

    constructor(transport_layer, allies_store, enemies_store) {
        this.allies_store = allies_store;
        this.enemies_store = enemies_store;
        this.current_combatant = null;

        this.transport_layer = transport_layer;

        this.transport_layer.set_current_combatant_id = (combatant_id) => {
            this.set_current_combatant_id(combatant_id);
        };
    }

    get me() {
        return this.allies_store.me;
    }

    get enemies() {
        return this.enemies_store.enemy_ids.map(enemy_id => {
            return this.enemies_store.enemies[enemy_id]
        });
    }

    get combatants() {
        return Object.assign({}, this.allies_store.allies_and_me, this.enemies_store.enemies);
    }

    get combatant_ids() {
        return this.allies_store.ally_and_my_ids.concat(this.enemies_store.enemy_ids);
    }

    @action set_current_combatant_id(combatant_id) {
        this.combatant_ids.map((id) => {
            this.combatants[id].up_to_bat = false;
        });

        this.combatants[combatant_id].up_to_bat = true;
    }
}
