from enum import Enum

import event
from shared import socketio, identity_manager

#on its own thread
from ui_manager import UIManager


class AdventureManager():
    def __init__(self, StartingEvent):
        # todo: we should probably pass in a party handler, and refactor everything to use it instead of room manager
        self.party = None
        self.ui_manager = UIManager()
        characters = list(identity_manager.get_combatants())
        self.change_event(StartingEvent(characters))
        self.count = 0 #take this hackey shit out later

    def change_event(self, event:"event.Event"):

        #separate input and output because input specifically needs a lock
        self.input_handler = event.get_input_listener()

        self.input_handler.delegate_client_request = \
            (lambda type, payload: self.handle_client_request(type, payload))
        
        self.current_event = event
        ui_updates = event.initialize_ui()
        self.ui_manager.update(ui_updates)
        #socketio.sleep(1)

    def handle_client_request(self, type, character):
        ui_updates = self.current_event.handle_client_request(type, character)
        self.ui_manager.update(ui_updates)

    def update(self):
        if(self.current_event.tick_type == event.TickType.real_time):
            self.real_time_update()
        else:
            self.turn_based_update()

    def real_time_update(self):
        if self.count == 0:
            ui_updates = self.current_event.initialize()
            self.ui_manager.update(ui_updates)
            self.count += 1
            socketio.sleep(5.5)
        else:
            input = self.input_handler.get_input()
            ui_updates = self.current_event.handle_input(input)
            self.ui_manager.update(ui_updates)

            if self.current_event.state == event.State.end:
                self.change_event(self.current_event.get_next_event())
            socketio.sleep(5.5)


    def turn_based_update(self):
        input = self.input_handler.get_input()
        if(input):
            ui_updates = self.current_event.handle_input(input)
            self.ui_manager.update(ui_updates)
            if self.current_event.state == event.State.end:
                self.change_event(self.current_event.get_next_event())