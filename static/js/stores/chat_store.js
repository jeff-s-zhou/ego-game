/**
 * Created by Jeffrey on 9/20/2016.
 */
/* @flow */

import {observable, autorun, action, computed} from "mobx";
import {TransportLayer} from "../transport_layer";
type transport_layer_type = typeof TransportLayer;

export class ChatStore {
    @observable messages :Message[];
    @observable outgoing_message :string;
    current_id : number;
    transport_layer :transport_layer_type;

    constructor(transport_layer:transport_layer_type) {
        this.outgoing_message = "";
        this.messages = [];
        this.current_id = 0;
        this.transport_layer = transport_layer;
        this.transport_layer.update_chat = (msg => this.update_chat(msg));
    }

    update_chat(msg: {name:string, text:string}) {
        console.log("updating chat");
        this.messages.push(new Message(msg.name, msg.text, this.current_id ));
        this.current_id ++;
    }

}

class Message {
    @observable name :string;
    @observable text :string;
    @observable id: number;

    constructor(name :string, text :string, id: number) {
        this.name = name;
        this.text = text;
        this.id = id;
    }
}