from enum import Enum
from time import time
from typing import Type, Dict

import event_interface
import input_listener
from shared import socketio

import ui_manager as ui


class State(Enum):
    initializing = "initializing"
    waiting = "waiting"
    running = "running"

class Timer():
    start_time = None
    def time_elapsed(self, duration):
        if not self.start_time:
            self.start_time = time()
            return False
        else:
            if (time() - self.start_time) > duration:
                self.start_time = None
                return True
            else:
                return False


#real time events only occur during adventures
class Adventure():
    def __init__(self, StartingEvent:Type["event_interface.EventInterface"], party):
        # todo: we should probably pass in a party handler, and refactor everything to use it instead of room manager
        self.ui_manager = ui.UIManager()
        self.input_listener = input_listener.InputListener()
        self.state = State.initializing
        self.count = 0 #TODO: take this hackey shit out later
        self.party = party
        self.change_event(StartingEvent(self.party))
        self.timer = Timer()

    def change_event(self, event:"event_interface.EventInterface"):
        self.state = State.waiting
        self.current_event = event
        ui_updates = event.initialize()
        self.ui_manager.update(ui_updates)
        socketio.sleep(1)
        self.state = State.running

    def delegate_input_handling(self, input:Dict):
        if input['class'] == "general":
            ui_updates = self.handle_input(input)
            self.ui_manager.update(ui_updates)
        else:
            ui_updates = self.current_event.handle_input(input)
            if ui_updates:
                self.ui_manager.update(ui_updates)

    def handle_input(self, input:Dict):
        if input['type'] == "initialize adventure":
            return self.initialize_adventure()


    def initialize_adventure(self):
        updates = []
        for character in self.party:
            my_static_state = character.get_static_state("self")
            ally_static_states = [ally.get_static_state("ally") for ally in character.allies] + [my_static_state]
            create_allies = ui.UIUpdate(ui.UIEvent.create_allies, ally_static_states, character)
            updates.append(create_allies)
        return updates


    def run(self):
        while(True):
            socketio.sleep(0) # TODO: WHYYYYYYYYYYYYYY
            client_input = self.input_listener.pop_from_queue()
            if client_input:
                self.delegate_input_handling(client_input)

            if self.state == State.running:
                if (self.current_event.tick_type == event_interface.TickType.real_time):
                    self.real_time_update()
                else:
                    self.turn_based_update()

            #usually when waiting to initialize an event
            elif self.state == State.waiting:
                pass


    def real_time_update(self):
        if self.timer.time_elapsed(5.5):
            ui_updates = self.current_event.update()
            self.ui_manager.update(ui_updates)

        if self.current_event.state == event_interface.State.end:
            self.change_event(self.current_event.get_next_event())


    def turn_based_update(self):
            ui_updates = self.current_event.update()
            self.ui_manager.update(ui_updates)
            if self.current_event.state == event_interface.State.end:
                self.change_event(self.current_event.get_next_event())