
import threading
from threading import Timer

import time

__author__ = 'Jeffrey'

from flask_restless import APIManager
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from shared import db
import models

from combat_manager import CombatManager
from combat_monitor import CombatMonitor
from room_manager import RoomManager
from ui_manager import UIManager
from combat_logger import CombatLogger

async_mode = None

app = Flask('ego', static_url_path='')
db.init_app(app)
socketio = SocketIO(app, async_mode=async_mode)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ego.db'

with app.app_context():
    db.create_all()
    api_manager = APIManager(app, flask_sqlalchemy_db=db)
    api_manager.create_api(models.Character, methods=['GET', 'DELETE', 'PUT', 'POST'])
    api_manager.create_api(models.Skill, methods=['GET'])
    api_manager.create_api(models.CharacterSkill, methods=['GET'])

room_manager = RoomManager()
ui_manager = UIManager(socketio, room_manager)
characters = room_manager.get_combatants()
combat_monitor = CombatMonitor()
combat_logger = CombatLogger()
combat_manager = CombatManager(list(characters), ui_manager, combat_monitor, combat_logger)
thread = None


def background():
    #TODO: replace this with waiting for all combatants to confirm initialization
    socketio.sleep(2)
    while True:
        combat_manager.update()
        socketio.sleep(5.5)
        combat_manager.handle_input()


@app.route('/')
def index():
    return render_template("index.html", async_mode=socketio.async_mode)


@socketio.on('disconnect', namespace='/test')
def log_disconnected():
    print('a user disconnected')
    # TODO: once every player disconnects, pickle the suspended state of the battle


@socketio.on('chat message', namespace='/test')
def emit_message(message):
    emit('chat message', message, broadcast=True, namespace='/test')


@socketio.on('connect', namespace='/test')
def log_connected():
    print("connected")
    character = room_manager.get_character(request.sid)
    # TODO: on refresh/rejoin, we get the current state of the game

    if room_manager.all_combatants_present():
        global thread
        if thread is None:
            thread = socketio.start_background_task(target=background)

'''
input:
    caster_id:
    skill_id:
    target_id:
'''
@socketio.on('turn input', namespace='/test')
def handle_input(input):
    combat_monitor.send_input(input)

#TODO
@socketio.on('fetch combatants', namespace='/test')
def fetch_combatants_for_sid():
    character = room_manager.get_character(request.sid)
    combat_manager.get_combatants_for_character(character)

if __name__ == '__main__':
    # app.run()
    socketio.run(app)























