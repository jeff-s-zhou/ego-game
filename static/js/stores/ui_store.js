/**
 * Created by Jeffrey on 9/22/2016.
 */

//general UI store for determining which components to display

import {observable} from "mobx";

export const EVENT_TYPE = {
    combat:"combat event"
};

//TODO: rename, this isn't really the UI store
export class UIStore {
    @observable event;

    constructor(transport_layer) {
        this.event = {type: null, initializers:{}};
        this.transport_layer = transport_layer;
        this.transport_layer.set_event = (event) => {
            this.set_event(event);
        }
    }

    set_event(event) {
        this.event = event;
    }
}


