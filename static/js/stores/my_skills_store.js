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
        this.transport_layer.update_my_skill_states = (skill_states) => {
            if(this.skill_ids.length == 0){
                this.load_skills(skill_states);
            }
            else {
                this.update_skills(skill_states);
            }

        }
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

    //cast the currently selected skill on the ID
    @action cast(caster_id, target_id) {
        this.transport_layer.handle_input(caster_id, this.selected.id, target_id);
        //TODO: this might not actually be threadsafe
        this.selected = null;
    }
}

export class Skill {
    @observable id;
    @observable name;
    @observable description;
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
        this.description = skill.description;
        this.condition = skill.condition;
        this.valid = skill.valid;
    }

    update(skill) {
        this.condition = skill.condition;
        this.valid = skill.valid;
    }
}