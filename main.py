__author__ = 'Jeffrey'

from flask_restless import APIManager
from flask import Flask, request, redirect, url_for, render_template, session, flash, jsonify
from flask_socketio import SocketIO, emit

from shared import db
from models import Character
from combat import get_precombat_state

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
    precombat_state = get_precombat_state(get_fake_char(player_count))
    emit('precombat', precombat_state)

    # last person in triggers game start
    # TODO: on refresh/rejoin, we get the current state of the game
    if (player_count > NUM_PLAYERS):
        emit('combat start', broadcast=True)


@socketio.on('disconnect')
def log_disconnected():
    print('a user disconnected')
    # TODO: once every player disconnects, pickle the suspended state of the battle


@socketio.on('chat message')
def test_message(message):
    emit('chat message', message, broadcast=True)
    print(message)


if __name__ == '__main__':
    # app.run()
    socketio.run(app)
