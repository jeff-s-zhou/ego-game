/**
 * Created by Jeffrey on 9/21/2016.
 */
import {observable, autorun, action, computed, reaction} from "mobx";

export class AlliesStore {
    @observable allies;
    @observable ally_ids;
    @observable me;
    @observable ally_and_my_ids;
    @observable allies_and_me;

    constructor(transport_layer) {
        this.allies = {};
        this.allies_and_me = {};
        this.ally_ids = [];
        this.ally_and_my_ids = [];
        this.me = null;

        this.dispose = autorun(() => {
            console.log("changing up to bat");
            if(this.me != null) {
                console.log(this.me.up_to_bat)
            }
        });

        this.transport_layer = transport_layer;

        this.transport_layer.create_allies = (allies) => {
            this.create_allies(allies)
        };

        this.transport_layer.update_ally_states = (ally_states) => {
            this.set_ally_states(ally_states)
        };
    }

    create_allies(allies) {
        allies.map((ally) => {
            if(ally.relation == "self"){
                console.log("adding me");
                this.me = new Ally(this, ally);
                this.allies_and_me[this.me.id] = this.me;
                this.ally_and_my_ids.push(this.me.id);
            }
            else {
                let new_ally = new Ally(this, ally);
                this.allies[ally.id] = new_ally; //...you have to set the dict first? then the array?
                this.allies_and_me[ally.id] = new_ally;

                this.ally_and_my_ids.push(ally.id);
                this.ally_ids.push(ally.id);
            }
        });
    }
    
    set_ally_states(ally_states) {
        ally_states.map((ally_state) => {
            this.allies_and_me[ally_state.id].update(ally_state);
        });
    }

    @action
    reset_selection() {
        this.ally_and_my_ids.map((combatant_id) => {
            this.allies_and_me[combatant_id].is_selected = false;
        })
    }
}

//implements selectable, implements turn_ordered
class Ally {
    @observable id;
    @observable name;
    @observable up_to_bat;
    @observable is_selected;
    @observable max_hp;
    @observable max_mp;
    @observable init_balance;
    @observable hp;
    @observable mp;
    @observable balance;
    @observable order;

    constructor(store, ally) {
        this.store = store;
        this.id = ally.id;
        this.name = ally.name;
        this.up_to_bat = false;
        this.is_selected = false;
        this.max_hp = ally.stats.max_hp;
        this.max_mp = ally.stats.max_mp;
        this.init_balance = ally.stats.init_balance;
        this.hp = 0;
        this.mp = 0;
        this.balance = 0;
        this.order = 0;
    }

    update(ally) {
        this.hp = ally.state.hp;
        this.mp = ally.state.mp;
        this.balance = ally.state.balance;
        this.order = ally.state.order;
        //this.statuses = ally.statuses; TODO
    }

    @action
    select() {
        this.store.reset_selection();
        this.is_selected = true;
    }
}