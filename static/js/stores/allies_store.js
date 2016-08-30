/**
 * Created by Jeffrey on 8/29/2016.
 */

import {observable, autorun, action} from "mobx";

export class AlliesStore {
    @observable allies;
    @observable selected;
    @observable ally_ids;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.allies = {};
        this.ally_ids = [];
        this.transport_layer.update_allies_state = (allies_state) => {
            console.log("hit the new event");
            this.update_allies(allies_state)
        };
        this.transport_layer.fetch_allies();
    }

    update_allies(allies) {
        if(this.ally_ids.length == 0){
            allies.map((ally) => {
                this.allies[ally.id] = new Ally(this, ally);
                this.ally_ids.push(ally.id);
            });
        }

        else {
            allies.map((ally) => {
                this.allies[ally.id].update(ally);
            });
        }
    }
}


class Ally {
    @observable id;
    @observable name;
    @observable statuses;

    constructor(store, ally) {
        this.store = store;
        this.id = ally.id;
        this.name = ally.name;
        this.hp = ally.hp;
        this.mp = ally.mp;

        //this.statuses = ally.statuses; TODO
    }

    update(ally) {
        console.log("updating ally");
        this.hp = ally.hp;
        this.mp = ally.mp;

        //this.statuses = ally.statuses; TODO
    }
}