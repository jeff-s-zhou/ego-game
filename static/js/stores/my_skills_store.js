/**
 * Created by Jeffrey on 8/29/2016.
 */

import {observable, autorun, action} from "mobx";

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