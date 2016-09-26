from threading import Lock
from flask import request
from shared import socketio, identity_manager


class CombatInputListener:
    def __init__(self):
        self.delegate_client_request = (lambda x: print("error in CombatInputHandler"))
        self.turn_lock = Lock()
        self.turn_input = None
        socketio.on_event('turn input', self.handle_turn_input, namespace='/test')
        socketio.on_event('combat client request', self.handle_client_request, namespace='/test')

    def get_input(self):
        with self.turn_lock:
            temp = self.turn_input
            self.turn_input = None
            return temp

    def handle_turn_input(self, turn_input):
        with self.turn_lock:
            self.turn_input = turn_input

    def handle_client_request(self, request_type):
        with self.turn_lock:
            character = identity_manager.get_character(request.sid)
            self.delegate_client_request(request_type, character)