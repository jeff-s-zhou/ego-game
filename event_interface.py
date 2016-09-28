from enum import Enum
from typing import List, Dict, Union

import character
import ui_manager


class State(Enum):
    start = "start"
    running = "running"
    end = "end"

class TickType(Enum):
    real_time = "real time"
    wait_for_input = "wait for input"

#TODO: raise exceptions
class EventInterface:
    def __init__(self, player_characters:"character.Character", event_type):
        self.tick_type = None
        self.state = None

    #sends respective command to ui so it knows what components to load
    def initialize(self) -> List[ui_manager.UIUpdate]:
        pass

    def update(self) -> List[ui_manager.UIUpdate]:
        pass

    def handle_input(self, input:Dict) -> Union[List[ui_manager.UIUpdate], None]:
        pass

    def get_next_event(self) -> 'EventInterface':
        pass

