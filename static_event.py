import event_interface
import ui_manager as ui

class StaticEvent(event_interface.EventInterface):
    def __init__(self, player_characters, event_type):
        super().__init__(player_characters, event_type)
        self.state = event_interface.State.start
        self.tick_type = event_interface.TickType.wait_for_input
        self.name = event_type.name
        self.initial_text = event_type.initial_text
        self.state_change = event_type.state_change
        self.next_event = event_type.next_event


    def initialize(self):
        return [ui.UIUpdate(ui.UIEvent.set_event, ui.EventType.static_event.value)]

    def update(self):
        pass

    def handle_input(self, input):
        pass

    def initialize(self):
        pass

    def get_next_event(self):
        pass