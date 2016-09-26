/**
 * Created by Jeffrey on 9/24/2016.
 */


export class TransportLayer {

    constructor(socket) {
        this.socket = socket;
        this.set_ui_state = ((ui_state) => null);
        this.create_allies = ((allies) => null);
        this.update_ally_states = ((ally_states) => null);
        this.update_chat = ((msg => null));

        socket.on('ui state', (ui_state) => {
            console.log("transport_layer handling ui state");
            this.set_ui_state(ui_state);
        });

        socket.on('create allies', (allies) => {
            this.create_allies(allies);
        });

        socket.on('my ally states', (allies_states) => {
            this.update_ally_states(allies_states);
        });

        socket.on('chat message', (msg) => {
            this.update_chat(msg);
        });
    }

    ready() {
        this.socket.emit('client request', 'adventure ready');
    }

    send_msg(name, text) {
        this.socket.emit('chat message', {name: name, text: text});
    }
}