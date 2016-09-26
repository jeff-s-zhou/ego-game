
import threading
from threading import Timer

import time


__author__ = 'Jeffrey'


from flask_restless import APIManager
from flask import Flask, render_template, request
from flask_socketio import emit
from combat_event import CombatEvent
from adventure_manager import AdventureManager
import models


from shared import db, app, socketio, identity_manager

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ego.db'

with app.app_context():
    db.create_all()
    api_manager = APIManager(app, flask_sqlalchemy_db=db)
    api_manager.create_api(models.Character, methods=['GET', 'DELETE', 'PUT', 'POST'])
    api_manager.create_api(models.Skill, methods=['GET'])
    api_manager.create_api(models.CharacterSkill, methods=['GET'])


thread = None
adventure_manager = None

def background():
    #TODO: replace this with waiting for all combatants to confirm initialization
    adventure_manager = AdventureManager(CombatEvent)
    socketio.sleep(1)
    while True:
        adventure_manager.update()


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

@socketio.on('client request', namespace='/test')
def handle_client_request(request_type):
    if(request_type == "adventure ready"):
        identity_manager.register_sid_with_account(request.sid)
        if identity_manager.all_combatants_present():
            global thread
            if thread is None:
                thread = socketio.start_background_task(target=background)


@socketio.on('connect', namespace='/test')
def log_connected():
    pass
    # TODO: on refresh/rejoin, we get the current state of the game




if __name__ == '__main__':
    # app.run()
    socketio.run(app)























