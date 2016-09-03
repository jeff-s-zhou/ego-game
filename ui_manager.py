class UIManager:
    def __init__(self, socketio, room_manager):
        self.socketio = socketio
        self.room_manager = room_manager

    def combat_start(self):
        self.socketio.emit('combat start', 'start', broadcast=True, namespace='/test')

    def update_pre_combat(self):
        #basic user info? currently loaded from database
        #basic enemy info, ally info
        #basic skill info? currently loaded from database
        #I got it. How about we slap this into the lifecycle event too?
        #maybe this should be going into the input handler?
        pass

    def update_turn_for(self, combatant, current_combatant, allies_state, enemies_state):
        sid = self.room_manager.get_sid(combatant)
        my_combat_state = combatant.get_state()
        self.socketio.emit('my combat state', my_combat_state, room=sid, namespace='/test')
        self.socketio.emit('allies state', allies_state, room=sid, namespace='/test')
        self.socketio.emit('enemies state', enemies_state, room=sid, namespace='/test')
        self.socketio.emit('current turn', current_combatant.id, broadcast=True, namespace='/test')


    def update_round(self):
        pass

    def update_turn_order(self):
        pass
