/**
 * Created by Jeffrey on 8/29/2016.
 */
import {observable, autorun, action} from "mobx";

export class EnemiesStore {
    @observable enemies;
    @observable enemy_ids;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.enemies = {};
        this.enemy_ids = [];
        this.transport_layer.update_enemies_state = (enemies_state) => {
            this.update_enemies(enemies_state)
        };
        this.transport_layer.fetch_enemies();
    }

    update_enemies(enemies) {
        if(this.enemy_ids.length == 0){
            enemies.map((enemy) => {
                this.enemies[enemy.id] = new Enemy(this, enemy);
                this.enemy_ids.push(enemy.id);
            });
        }

        else {
            enemies.map((enemy) => {
                this.enemies[enemy.id].update(enemy);
            });
        }
    }
}


class Enemy {
    @observable id;
    @observable name;
    @observable statuses;

    constructor(store, enemy) {
        this.store = store;
        this.id = enemy.id;
        this.name = enemy.name;

        //this.statuses = enemy.statuses; TODO
    }

    update(enemy) {
        this.name = enemy.name;


        //this.statuses = enemy.statuses; TODO
    }
}