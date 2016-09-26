/**
 * Created by Jeffrey on 8/29/2016.
 */

import {observable, autorun, action, computed} from "mobx";

export class SkillsStore {
    @observable skills;
    @observable selected;
    @observable skill_ids;

    constructor(transport_layer, combatants_store) {
        this.transport_layer = transport_layer;
        this.combatants_store = combatants_store;
        this.skills = {};
        this.selected = null;
        this.skill_ids = [];
        this.transport_layer.update_my_skill_states = (skill_states) => {
            if (this.skill_ids.length == 0) {
                this.load_skills(skill_states);
            }
            else {
                this.update_skills(skill_states);
            }

        }
    }

    load_skills(skills) {
        console.log("loading skills");
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

    @action
    reset_selection() {
        this.skill_ids.map((skill_id) => {
            this.skills[skill_id].is_selected = false;
        })
    }

    //cast the currently is_selected skill on the ID
    @action cast(caster, target) {
        this.transport_layer.handle_input(caster.id, this.selected.id, target.id);
        //TODO: this might not actually be threadsafe
        this.selected.is_selected = false;
        this.selected = null;
        target.is_selected = false;
    }

    @computed get action_ids() {
        return this.skill_ids;
    }

    @computed get actions() {
        return this.skills;
    }

    get targets() {
        if (this.selected == null) {
            return this.combatants_store.enemies
        }
        else {
            let ids = this.selected.target_ids;
            let combatants = this.combatants_store.combatants;
            return ids.map((combatant_id) => {
                return combatants[combatant_id]
            });
        }
    }
}

export class Skill {
    @observable id;
    @observable name;
    @observable description;
    @observable condition;
    @observable valid;
    @observable is_selected;
    @observable target_ids;

    constructor(store, skill) {
        this.store = store;
        this.id = skill.id;
        this.name = skill.name;
        this.description = skill.description;
        this.condition = skill.condition;
        this.valid = skill.valid;
        this.is_selected = false;
        this.target_ids = skill.target_ids;
    }

    update(skill) {
        this.condition = skill.condition;
        this.valid = skill.valid;
        //TODO: add regular updating of valid_target_ids
        //this.valid_target_ids = skill.valid_targets;
    }

    @action
    select() {
        this.store.reset_selection();
        this.store.selected = this;
        this.is_selected = true;
    }

    @computed get text() {
        return this.name + " " + this.condition
    }
}