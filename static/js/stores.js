/**
 * Created by Jeffrey on 8/27/2016.
 */

import {observable, autorun, action} from "mobx";


export class MyCharacterStore {
    @observable name;
    @observable id;
    @observable hp;
    @observable mana;
    @observable active_skills;
    @observable statuses;

    constructor(transport_layer, active_skills) {
        this.transport_layer = transport_layer;
        this.transport_layer.update_my_combat_state = ((combat_state) => this.update_my_character(combat_state));
        this.name = "";
        this.id = 0;
        this.hp = 0;
        this.mana = 0;
        this.active_skills = active_skills;
        this.statuses = [];
        this.disposer = autorun(() => console.log("my hp is now " + this.hp));
        this.transport_layer.fetch_my_character();
    }

    update_my_character(state) {
        if(this.id === 0) {
            this.name = state.name;
            this.id = state.id;
            this.hp = state.hp;
            this.mana = state.mana;
            this.active_skills.load_skills(state.active_skills);
            //TODO: statuses
        }
        else {
            console.log("calling update my character");
            this.hp = state.hp;
            this.mana = state.mana;
            this.active_skills.update_skills(state.active_skills);
            //TODO: statuses
        }


    }
}

export class SkillsStore {
    @observable skills;
    @observable selected;
    @observable skill_ids;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.skills = {};
        this.selected = null;
        this.skill_ids = [];
        this.disposer = autorun(() => console.log("selected is now " + this.selected));
    }

    load_skills(skills) {
        skills.map((skill) => {
            this.skills[skill.id] = new Skill(this, skill);
            this.skill_ids.push(skill.id);
        });
    }

    update_skills(skills) {
        skills.map((skill) => {
            this.skills[skill.id].update(skill);
        });
        console.log("updating skills");
        console.log(this.skills);
    }
}

export class Skill {
    @observable id;
    @observable name;
    @observable condition;
    @observable valid;

    @action
    select() {
        this.store.selected = this;
        console.log(this);
    }

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
            this.targets[target.id] = new Target(this, target);
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



