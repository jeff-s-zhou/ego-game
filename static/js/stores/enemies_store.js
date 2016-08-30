/**
 * Created by Jeffrey on 8/29/2016.
 */

import {observable, autorun, action} from "mobx";

export class TargetsStore {
    @observable targets;
    @observable selected;
    @observable target_ids;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.targets = {};
        this.target_ids = [];
        this.selected = null;

        this.disposer = autorun(() => console.log())
    }

    load_targets(targets) {
        targets.map((target) => {
            this.targets[target.id] = new Target(this, target);
            this.target_ids.push(target.id);
        });
    }

    update_targets(targets) {
        targets.map((target) => {
            this.targets[target.id].update(target);
        });
    }
}


class Target {
    @observable id;
    @observable name;
    @observable statuses;

    constructor(store, target) {
        this.store = store;
        this.id = target.id;
        this.name = target.name;
        this.statuses = target.statuses;
    }

    update(target) {
        this.id = target.id;
        this.name = target.name;
        this.statuses = target.statuses;
    }


    select(caster, skill) {
        this.store.selected = this;
        this.store.transport_layer.handle_turn_input(caster.id, skill.id, this.id)
    }
}
