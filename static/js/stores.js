/**
 * Created by Jeffrey on 8/27/2016.
 */

import {observable} from "mobx";


/*
character state:
    name:
    id:
    hp:
    mana:
    statuses:[
        status:
            type:
            name:
            duration OR cooldown:
    ]
    active_skills:[
        skill:
            id:
            name:
            cooldown:
            valid:
    ]
*/

export class MyCharacterStore {
    @observable name;
    @observable id;
    @observable hp;
    @observable mana;
    @observable active_skills;
    @observable statuses;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.name = "";
        this.id = 0;
        this.hp = 0;
        this.mana = 0;
        this.active_skills = MySkillsStore(transport_layer);
        this.statuses = [];
    }

    loadMyCharacter() {
        this.transport_layer.fetch_my_character().then((fetched_character) => {
            this.name = fetched_character.name;
            this.id = fetched_character.id;
            this.hp = fetched_character.hp;
            this.mana = fetched_character.mana;
            this.active_skills.set_skills(fetched_character.active_skills)
            //this.statuses.set_statuses(fetched_character.statuses);
        })
    }
}

export class MySkillsStore {
    @observable skills;
    @observable selected;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.skills = [];
        this.selected = null;
    }

    set_skills(skills) {
        this.skills = skills.map((skill) => {return Skill(this, skill)});
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

    select() {
        this.store.selected = this;
    }
}

export class TargetsStore {
    @observable targets;
    @observable selected;

    constructor(transport_layer) {
        this.transport_layer = transport_layer;
        this.targets = [];
        this.selected = null;

        this.disposer = autorun(() => console.log())
    }

    set_targets(targets) {
        this.targets = targets.map((target) => {return Target(this, target)});
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

    select(caster, skill) {
        this.store.selected = this;
        this.store.transport_layer.handle_turn_input(caster.id, skill.id, this.id)
    }
}



