/**
 * Created by Jeffrey on 8/29/2016.
 */


import {observable, autorun, action, computed, reaction} from "mobx";
import {target_types} from "../globals";

export class CombatantsStore {
    @observable allies;
    @observable ally_ids;
    @observable enemies;
    @observable enemy_ids;
    @observable me;
    @observable combatants;
    @observable combatant_ids;

    constructor(transport_layer) {
        this.allies = {};
        this.ally_ids = []; //need to set these lists before respective objects because of react
        this.enemies = {};
        this.enemy_ids = [];
        this.me = null;
        this.combatants = {};
        this.combatant_ids = [];
        this.current_combatant = null;

        this.transport_layer = transport_layer;
        this.transport_layer.fetch_combatants();

        this.transport_layer.set_current_combatant_id = (combatant_id) => {
            this.set_current_combatant_id(combatant_id);
        };
        //TODO: need to wait to update until create is called first
        this.transport_layer.update_combatant_states = (combatant_states) => {
            this.set_combatant_states(combatant_states)
        };

        this.transport_layer.create_combatants = (combatants) => {
            this.create_combatants(combatants)
        };
    }

    set_current_combatant_id(combatant_id) {
        this.combatant_ids.map((id) => {
            this.combatants[id].up_to_bat = false;
        });

        this.combatants[combatant_id].up_to_bat = true;
    }

    create_combatants(combatants) {
        combatants.map((combatant) => {
            if(combatant.relation == "self"){
                this.me = new Ally(this, combatant);
                this.combatants[combatant.id] = this.me;
                this.combatant_ids.push(combatant.id);

            }
            else if(combatant.relation == "ally"){
                var ally = new Ally(this, combatant);
                this.allies[combatant.id] = ally; //...you have to set the dict first? then the array?
                this.ally_ids.push(combatant.id);
                this.combatants[combatant.id] = ally;
                this.combatant_ids.push(combatant.id);

            }
            else if(combatant.relation == "enemy"){
                var enemy = new Enemy(this, combatant);
                this.enemies[combatant.id] = enemy;
                this.combatants[combatant.id] = enemy;
                this.combatant_ids.push(combatant.id);
                this.enemy_ids.push(combatant.id);
            }
        });
    }

    set_combatant_states(combatant_states) {
        combatant_states.map((combatant_state) => {
            this.combatants[combatant_state.id].update(combatant_state);
        });
    }

    //depending on the target type of the skill selected, we display different targets
    //TODO: more complicated logic for multiple target types
    get_targets(t_types) {
        var targets = t_types.map(t_type => {
            switch(t_type) {
                case target_types.single_enemy:
                    return this.enemy_ids.map((enemy_id) => {
                        return this.enemies[enemy_id];
                    });
                case target_types.single_ally:
                    console.log("handling ally case");
                    return this.ally_ids.map((ally_id) => {
                        return this.allies[ally_id];
                    });
                default:
                    console.log("ERROR: default case met in CombatantsStore.get_targets");
                    return [];
            }
        });
        //flatten the array of arrays
        return [].concat.apply([], targets);
    }

    @action
    reset_selection() {
        this.combatant_ids.map((combatant_id) => {
            this.combatants[combatant_id].selected = false;
        })
    }
}

class Combatant{
    @observable id;
    @observable name;
    @observable up_to_bat;
    @observable selected;

    constructor(store, combatant) {
        this.store = store;
        this.id = combatant.id;
        this.name = combatant.name;
        this.up_to_bat = false;
        this.selected = false;
    }

    @action
    select() {
        this.store.reset_selection();
        this.selected = true;
    }
}

class Ally extends Combatant {
    @observable max_hp;
    @observable max_mp;
    @observable init_balance;
    @observable hp;
    @observable mp;
    @observable balance;
    @observable order;

    constructor(store, ally) {
        super(store, ally);
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
}

export class Enemy extends Combatant {
    @observable hp;
    @observable mp_estimate;
    @observable balance_estimate;
    @observable order;

    //TODO: decide on using hp estimate or not
    constructor(store, enemy) {
        super(store, enemy);
        this.max_hp = 10;
        this.hp = 0;
        this.mp_estimate = 0;
        this.balance_estimate = 0;
        this.order = 0;
    }

    update(enemy) {
        //TODO: fix this hackyness
        this.hp = enemy.state.hp_estimate;
        this.mp_estimate = enemy.state.mp_estimate;
        this.balance_estimate = enemy.state.balance_estimate;
        this.order = enemy.state.order;

    }
}
