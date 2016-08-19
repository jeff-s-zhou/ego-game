def UIManager():
    def __init__(self, socketio, room_manager):
        self.socketio = socketio
        self.room_manager = room_manager

    def update_state_for(self, character, personal_state):
        sid = self.room_manager.get_sid(character)
        self.socketio.emit('my combat state', personal_state, room=sid)

    def update_state(self, state):
        self.socketio.emit('pre combat state', combat_state, broadcast=True)
        self.socketio.emit('combat start', 'start', broadcast=True)
        start_character = combat_manager.get_current_combatant()
        self.socketio.emit('current turn', start_character.name, broadcast=True)
