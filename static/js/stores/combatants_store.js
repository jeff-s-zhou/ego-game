/**
 * Created by Jeffrey on 8/29/2016.
 */


import {observable, autorun, action, computed} from "mobx";

export class CombatantsStore {
    @observable allies_store;
    @observable enemies_store;

    constructor(transport_layer, allies_store, enemies_store) {
        this.transport_layer = transport_layer;
        this.allies_store = allies_store;
        this.enemies_store = enemies_store;
    }

    //depending on the target type of the skill selected, we display different targets
    //TODO actually have it depend on targets
    get_targets(target_selector) {
        var targets = [];
        this.enemies_store.enemy_ids.map((enemy_id) => {
            targets.push(this.enemies_store.enemies[enemy_id]);
        });
        return targets;
    }
}
