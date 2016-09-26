/**
 * Created by Jeffrey on 9/22/2016.
 */

//general UI store for determining which components to display

import {observable} from "mobx";

export const EVENT_TYPE = {
    combat:"combat"
};

export class UIStore {
    @observable event_type;

    constructor(transport_layer) {
        this.event_type = null;
        this.transport_layer = transport_layer;
        this.transport_layer.set_ui_state = (ui_state) => {
            this.set_state(ui_state);
        }
    }

    set_state(state) {
        console.log("updating from ui store");
        this.event_type = state;
    }
}