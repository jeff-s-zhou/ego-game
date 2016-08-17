from threading import Timer

__author__ = 'Jeffrey'

from flask_restless import APIManager
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from shared import db
from models import Character

from combat_manager import CombatManager
from combat_monitor import CombatMonitor

app = Flask('ego', static_url_path='')
db.init_app(app)
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ego.db'

with app.app_context():
    db.create_all()
    api_manager = APIManager(app, flask_sqlalchemy_db=db)
    api_manager.create_api(Character, methods=['GET', 'DELETE', 'PUT', 'POST'])

room_manager = RoomManager()
characters = room_manager.get_combatants()
combat_manager = CombatManager(characters)
combat_monitor = CombatMonitor(combat_manager)


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('disconnect')
def log_disconnected():
    print('a user disconnected')
    # TODO: once every player disconnects, pickle the suspended state of the battle

@socketio.on('chat message')
def emit_message(message):
    emit('chat message', message, broadcast=True)



@socketio.on('connect')
def log_connected():
    character = room_manager.get_character(request.sid)
    # TODO: on refresh/rejoin, we get the current state of the game

    pre_combat_state = combat_manager.get_state_for(character)
    emit('pre combat state', pre_combat_state, room=request.sid)

    if(room_manager.all_combatants_present()):
        emit('combat start', broadcast=True)
        start_character = combat_manager.get_current_combatant()
        sid = room_manager.get_sid(start_character)
        emit('your turn', room=sid)
        Timer(5.0, times_up(start_character.character_name))


'''
input:
    caster_name:
    skill_name:
    target_name:
'''
@socketio.on('turn_input')
def handle_turn_input(turn_input):
    #TODO: make sure it's the right session, right character, valid skill, etc.
    success = combat_monitor.send_input(turn_input, turn_input.name)
    if success:

        for combatant in combat_manager.combatants:
            sid = room_manager.get_sid(combatant)
            my_combat_state = combat_manager.get_state_for(combatant)
            emit('my combat state', my_combat_state, room=sid)

        combat_state = combat_manager.get_state()
        emit('combat state', combat_state, broadcast=True)
        current_character = combat_manager.get_current_combatant()
        sid = room_manager.get_sid(current_character)
        emit('current turn', current_character.name, broadcast=True)
        Timer(5.0, times_up(current_character.character_name))


def times_up(character_name):
    success = combat_monitor.signal_times_up(character_name)
    if success:
        current_character = combat_manager.get_current_combatant()
        socketio.emit('current turn', current_character.name, broadcast=True)
        Timer(5.0, times_up(current_character.character_name))



'''
state:
    [
        character:
            name:
            id:
            hp:
            mana:
            statuses:[
                status:
                    type:
                    name:
                    duration OR cooldown:
            ]
            active_skills:[
                skill:
                    name:
                    cooldown:
            ]
    ]
'''

if __name__ == '__main__':
    # app.run()
    socketio.run(app)























