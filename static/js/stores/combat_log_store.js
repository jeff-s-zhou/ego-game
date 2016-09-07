/**
 * Created by Jeffrey on 9/4/2016.
 */

import {observable, autorun, action} from "mobx";

export class CombatLogStore {
    @observable turn_entries;

    constructor(transport_layer) {
        this.turn_entries = [];
        this.transport_layer = transport_layer;

        this.transport_layer.update_log = ((entry) => {
            this.update_log_entries(entry)
        });

        this.transport_layer.fetch_log();
    }

    update_log_entries(entry) {
        this.turn_entries.push(new TurnEntry(entry))
    }
}

class TurnEntry{
    @observable pre_reactions;
    @observable skill_cast;
    @observable payloads_and_post_reactions;

    constructor(entry){
        this.pre_reactions = entry.pre_reactions;
        this.skill_cast = entry.skill_cast;
        this.payloads_and_post_reactions = entry.payloads_and_post_reactions;
    }
}