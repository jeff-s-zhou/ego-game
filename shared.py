__author__ = 'Jeffrey'

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from identity_manager import IdentityManager

db = SQLAlchemy()
app = Flask('ego', static_url_path='')
db.init_app(app)
async_mode = None
socketio = SocketIO(app, async_mode=async_mode)

identity_manager = IdentityManager()