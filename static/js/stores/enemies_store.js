/**
 * Created by Jeffrey on 9/21/2016.
 */
import {observable, autorun, action, computed, reaction} from "mobx";

export class EnemiesStore {
    @observable enemies;
    @observable enemy_ids;

    constructor(transport_layer) {
        this.enemies = {};
        this.enemy_ids = [];

        this.transport_layer = transport_layer;

        this.transport_layer.create_enemies = (enemies) => {
            this.create_enemies(enemies)
        };
        this.transport_layer.update_enemy_states = (enemy_states) => {
            this.set_enemy_states(enemy_states)
        };
    }

    create_enemies(enemies) {
        enemies.map((enemy) => {
            this.enemies[enemy.id] = new Enemy(this, enemy);
            this.enemy_ids.push(enemy.id);
        });
    }

    set_enemy_states(enemy_states) {
        enemy_states.map((enemy_state) => {
            this.enemies[enemy_state.id].update(enemy_state);
        });
    }

    @action
    reset_selection() {
        this.enemy_ids.map((enemy_id) => {
            this.enemies[enemy_id].is_selected = false;
        })
    }
}

//implements selectable, implements turn_ordered
export class Enemy{
    @observable id;
    @observable name;
    @observable up_to_bat;
    @observable is_selected;
    @observable hp;
    @observable mp_estimate;
    @observable balance_estimate;
    @observable order;

    //TODO: decide on using hp estimate or not
    constructor(store, enemy) {
        this.store = store;
        this.id = enemy.id;
        this.name = enemy.name;
        this.up_to_bat = false;
        this.is_selected = false;
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

    @action
    select() {
        this.store.reset_selection();
        this.is_selected = true;
    }
}

