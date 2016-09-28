from threading import Lock
from flask import request
from shared import socketio, identity_manager




class InputListener:
    def __init__(self):
        self.delegate_client_request = (lambda x: print("error in CombatInputHandler"))
        self.lock = Lock()
        self.input_queue = []
        socketio.on_event('input', self.push_on_queue, namespace='/test')


    def pop_from_queue(self):
        with self.lock:
            if self.input_queue:
                return self.input_queue.pop()
            else:
                return None

    def push_on_queue(self, input):
        print("pushed on queue")
        with self.lock:
            self.input_queue.append(input)