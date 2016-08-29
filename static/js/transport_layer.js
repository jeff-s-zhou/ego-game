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

    constructor(socket) {
        this.socket = socket;

        this.notify_current_turn = ((character_name) => null);
        this.update_allies_state = ((allies_state) => null);
        this.update_enemies_state = ((enemies_state) => null);
        this.update_my_combat_state = ((combat_state) => console.log("still using old function"));

        socket.on('connect', () => {console.log("connected");});

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

        socket.on('my combat state', (my_combat_state) => {
            this.update_my_combat_state(my_combat_state)
        });



    }

    fetch_my_character() {
        this.socket.emit('fetch my character');
    }
}
