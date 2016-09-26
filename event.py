from enum import Enum

import character


class State(Enum):
    start = "start"
    end = "end"

class TickType(Enum):
    real_time = "real time"
    wait_for_input = "wait for input"


class Event:
    def __init__(self, tick_type:TickType, player_characters:"character.Character"):
        self.state = State.start
        self.tick_type = tick_type
        self.player_characters = player_characters

    #sends respective command to ui so it knows what components to load
    def initialize_ui(self):
        pass

    def handle_client_request(self, type, character):
        pass

    def get_input_listener(self):
        pass

    def handle_input(self, input):
        pass

    #initial event update
    def initialize(self):
        pass

    def get_next_event(self):
        pass

