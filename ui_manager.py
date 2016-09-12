class UIManager:
    def __init__(self, socketio, room_manager):
        self.socketio = socketio
        self.room_manager = room_manager

    def create_combatants_for(self, character, combatant_static_states):
        sid = self.room_manager.get_sid(character)
        self.socketio.emit('create combatants', combatant_static_states, room=sid, namespace='/test')

    def combat_start(self):
        self.socketio.emit('combat start', 'start', broadcast=True, namespace='/test')

    def update_pre_combat(self):
        #basic user info? currently loaded from database
        #basic enemy info, ally info
        #basic skill info? currently loaded from database
        #I got it. How about we slap this into the lifecycle event too?
        #maybe this should be going into the input handler?
        pass

    def update_turn_for(self, combatant, combatant_states, my_skill_states, current_combatant):
        sid = self.room_manager.get_sid(combatant)
        self.socketio.emit('my skill states', my_skill_states, room=sid, namespace='/test')
        self.socketio.emit('combatant states', combatant_states, room=sid, namespace='/test')
        self.socketio.emit('current turn', current_combatant.id, room=sid, namespace='/test')

    def update_log(self, turn_log):
        self.socketio.emit('turn log', turn_log, broadcast=True, namespace='/test')

    def update_round(self):
        pass

    def update_turn_order(self):
        pass


