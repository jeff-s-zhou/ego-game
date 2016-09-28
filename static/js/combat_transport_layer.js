/**
 * Created by Jeffrey on 8/27/2016.
 */

export class CombatTransportLayer {

    constructor(socket) {
        this.socket = socket;
        this.set_current_combatant_id = ((character_name) => null);
        this.create_enemies = ((enemies) => null);
        this.update_enemy_states = ((enemy_states) => null);
        this.update_my_skill_states = ((my_skills) => console.log("update my skills not registered"));
        this.update_log = ((entry) => null);

        socket.on('current turn', (combatant_id) => {
            this.set_current_combatant_id(combatant_id);
        });

        socket.on('create enemies', (enemies) => {
            this.create_enemies(enemies);
        });

        socket.on('my enemy states', (enemies_states) => {
            this.update_enemy_states(enemies_states);
        });

        socket.on('my skill states', (skill_states) => {
            this.update_my_skill_states(skill_states)
        });

        socket.on('turn log', (turn_log) => {
            this.update_log(turn_log);
        });
    }

    handle_input(caster_id, skill_id, target_id) {
        let value = {caster_id:caster_id, skill_id:skill_id, target_id:target_id};
        this.socket.emit('input', {class: 'combat', type: 'turn input', value: value})
    }


    fetch_log() {
        this.socket.emit('fetch log');
    }

    //remove all socketio listeners
    dismantle() {

    }
}
