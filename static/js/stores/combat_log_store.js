/**
 * Created by Jeffrey on 9/4/2016.
 */

import {observable, autorun, action, computed} from "mobx";

export class CombatLogStore {
    @observable rounds;

    constructor(transport_layer) {
        this.rounds = [];
        this.transport_layer = transport_layer;

        this.transport_layer.update_log = ((entry) => {
            this.update_log_entries(entry)
        });

        this.transport_layer.fetch_log();
    }

    update_log_entries(entry) {

        var current_round; //TODO: do we want to make this an observable?
        //entry.round_index is 1 indexed
        if (entry.round_index > this.rounds.length) {
            current_round = new Round(this, entry.round_index);
            this.rounds.push(current_round)
        }
        else {
            current_round = this.rounds[entry.round_index - 1]
        }
        current_round.add_entry(entry);
    }

    @action reset_selection() {
        this.rounds.map((round) => {
            round.selected = false;
        })

    }

    @computed get current_turn() {
        if(this.rounds.length == 0) {
            return null;
        }
        var turn_entries_index = this.rounds[this.rounds.length - 1].turn_entries.length - 1;
        return this.rounds[this.rounds.length - 1].turn_entries[turn_entries_index]
    }


}

class Round {
    @observable index;
    @observable turn_entries;
    @observable selected; //TODO: might wanna move this to the react component

    constructor(store, index) {
        this.store = store;
        this.index = index;
        this.turn_entries = [];
        this.selected = false;
        this.select();
    }

    add_entry(entry) {
        this.turn_entries.push(new TurnEntry(entry));
    }

    @action select(){
        this.store.reset_selection();
        this.selected = true;
    }

    @computed get name(){
        return "Round " + this.index;
    }
}

class TurnEntry{
    @observable pre_reactions;
    @observable skill_cast;
    @observable payloads_and_post_reactions;
    @observable index;
    @observable round_index;

    constructor(entry){
        this.index = entry.index;
        this.round_index = entry.round_index;
        this.pre_reactions = entry.pre_reactions;
        this.skill_cast = entry.skill_cast;
        this.payloads_and_post_reactions = entry.payloads_and_post_reactions;
    }
}