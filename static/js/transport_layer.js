/**
 * Created by Jeffrey on 8/27/2016.
 */

/*

    //TODO: get actual skill based on character id, and not spoofing
    loadSkillsFromServer() {
        JQuery.ajax({
            url: ("/api/skill"),
            contentType: "application/json",
            dataType: "json",
            cache: false,
            success: (data) => {
                var my_skills = {};
                data.objects.map((skill) => {
                    my_skills[skill.id] = skill
                });
                app_state.skills = my_skills;
            },
            error: (xhr, status, err) => {
                console.error("api/ego", status, err.toString());
            }
        });
    }
 */

export class TransportLayer {

    constructor() {
        var socket = require('socket.io-client')('http://' + document.domain + ':' + location.port + '/test');

        this.update_my_combat_state = ((my_combat_state) => null);
        this.notify_current_turn = ((character_name) => null);
        this.update_allies_state = ((allies_state) => null);
        this.update_enemies_state = ((enemies_state) => null);

        socket.on('connect', () => {console.log("connected");});
        socket.on('my combat state', (my_combat_state) => {
            this.update_my_combat_state(my_combat_state)
        });

        socket.on('current turn', (character_name) => {
            console.log(character_name);
            this.notify_current_turn(character_name);
        });

        //state for my team
        socket.on('allies state', (allies_state) => {
            this.update_allies_state(allies_state);
        });

        //state for enemies
        socket.on('enemies state', (enemies_state) => {
            //this.setState({enemies_state:enemies_state});
            this.update_enemies_state(enemies_state);
        });

    }

    fetch_my_character() {

    }
}
