/**
 * Created by Jeffrey on 8/27/2016.
 */

import {observable} from "mobx";


export class MyCharacterStore {
    @observable name;
    @observable id;
    @observable hp;
    @observable mana;
    @observable active_skills;
    @observable statuses;

    constructor(transport_layer, active_skills) {
        this.transport_layer = transport_layer;
        this.transport_layer.update_my_combat_state((combat_state) => this.update_my_character(combat_state));
        this.name = "";
        this.id = 0;
        this.hp = 0;
        this.mana = 0;
        this.active_skills = active_skills;
        this.statuses = [];
    }

    update_my_character(state) {
        this.hp = state.hp;
        this.mana = state.mana;
        this.active_skills.set_skills(state.skills);
        //TODO: statuses
    }

    load_my_character() {
        this.transport_layer.fetch_my_character().then((fetched_character) => {
            this.name = fetched_character.name;
            this.id = fetched_character.id;
            this.hp = fetched_character.hp;
            this.mana = fetched_character.mana;
            this.active_skills.update_skills(fetched_character.active_skills)
            //this.statuses.set_statuses(fetched_character.statuses);
        })
    }
}

export class SkillsStore {
    @observable skills;
    @observable selected;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.skills = {};
        this.selected = null;
    }

    load_skills(skills) {
        skills.map((skill) => {
            this.skills[skill.id] = Skill(this, skill);
        });

    }

    update_skills(skills) {
        skills.map((skill) => {
            this.skills[skill.id].update(skill);
        });
    }
}

class Skill {
    @observable id;
    @observable name;
    @observable condition;
    @observable valid;

    constructor(store, skill) {
        this.store = store;
        this.id = skill.id;
        this.name = skill.name;
        this.condition = skill.condition;
        this.valid = skill.valid;
    }

    update(skill) {
        this.id = skill.id;
        this.name = skill.name;
        this.condition = skill.condition;
        this.valid = skill.valid;
    }

    select() {
        this.store.selected = this;
    }
}

/*
    statuses:[
        status:
            type:
            name:
            duration OR cooldown:
    ]
*/


export class TargetsStore {
    @observable targets;
    @observable selected;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.targets = {};
        this.selected = null;

        this.disposer = autorun(() => console.log())
    }

    load_targets(targets) {
        targets.map((target) => {
            this.targets[target.id] = Target(this, target);
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



