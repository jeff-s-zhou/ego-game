/**
 * Created by Jeffrey on 8/27/2016.
 */

export class TransportLayer {

    constructor(socket) {
        this.socket = socket;

        this.set_current_combatant_id = ((character_name) => null);
        this.update_combatant_states = ((combatant_states) => null);
        this.update_my_skill_states = ((my_skills) => console.log("update my skills not registered"));
        this.update_log = ((entry) => null);
        this.create_combatants = ((combatant) => null);
        this.update_chat = ((msg => null));

        socket.on('connect', () => {console.log("connected");});

        socket.on('current turn', (combatant_id) => {
            this.set_current_combatant_id(combatant_id);
        });

        socket.on('combatant states', (combatant_states) => {
            this.update_combatant_states(combatant_states);
        });

        socket.on('create combatants', (combatants) => {
            this.create_combatants(combatants);
        });

        socket.on('my skill states', (skill_states) => {
            this.update_my_skill_states(skill_states)
        });

        socket.on('turn log', (turn_log) => {
            this.update_log(turn_log);
        });

        socket.on('chat message', (msg) => {
            this.update_chat(msg);
            //JQuery('#messages').append(JQuery('<li>').text(msg));
        });
    }

    handle_input(caster_id, skill_id, target_id) {
        this.socket.emit('turn input', {caster_id:caster_id, skill_id:skill_id, target_id:target_id})
    }

    fetch_combatants() {
        this.socket.emit('fetch combatants');
    }

    fetch_log() {
        this.socket.emit('fetch log');
    }

    send_msg(name, text) {
        this.socket.emit('chat message', {name: name, text: text});
    }


}
