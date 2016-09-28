import event_interface
import ui_manager as ui


class DynamicEvent(event_interface.EventInterface):
    def __init__(self, player_characters, event_type):
        super().__init__(player_characters, event_type)
        self.state = event_interface.State.start
        self.tick_type = event_interface.TickType.wait_for_input
        self.name = event_type.name
        self.next_event = event_type.next_event
        self.state_mapping = event_type.state_mapping

    def initialize(self):
        return [ui.UIUpdate(ui.UIEvent.set_event, ui.EventType.dynamic_event.value)]

    def update(self):
        pass

    def handle_input(self, input):
        pass

    def get_next_event(self):
        pass