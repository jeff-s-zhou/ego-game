from threading import Timer

__author__ = 'Jeffrey'

from flask_restless import APIManager
from flask import Flask, render_template
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

# TODO: need to make this shit threadsafe eventually
NUM_PLAYERS = 3
player_count = 0

combat_manager = CombatManager()
combat_monitor = CombatMonitor(combat_manager)

# delete
def get_fake_char(number):
    if number == 1:
        pass
    elif number == 2:
        pass
    elif number == 3:
        pass


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('connect')
def log_connected():
    global player_count
    player_count = player_count + 1
    # last person in triggers game start
    # TODO: on refresh/rejoin, we get the current state of the game
    if (player_count > NUM_PLAYERS):
        emit('combat start', broadcast=True)

@socketio.on('disconnect')
def log_disconnected():
    print('a user disconnected')
    # TODO: once every player disconnects, pickle the suspended state of the battle

@socketio.on('chat message')
def emit_message(message):
    emit('chat message', message, broadcast=True)

@socketio.on('turn_input')
def handle_turn_input(input):
    #TODO: make sure it's the right session, right character, etc.
    combat_monitor.send_input(current_combatant)

def times_up():
    combat_monitor.signal_times_up(current_combatant)

def emit_start_turn():
    socketio.emit('turn_start')
    Timer(5.0, times_up())

def emit_state(state):
    socketio.emit('some event', (state))

'''
input:
    character_name:
    skill_name:
    target_name:
'''

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
@socketio.on('turn_input')
def handle_turn_input(input):
    #check to make sure it's the user's turn with flask-login and current_user
    #check to make sure it's a valid move
    #check to make sure it's valid target
    pass



if __name__ == '__main__':
    # app.run()
    socketio.run(app)
