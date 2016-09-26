from enum import Enum

from shared import identity_manager, socketio

from typing import List, Union, Any


class CombatUIEvent(Enum):
    ui_state = "ui state"
    create_allies = "create allies"
    my_ally_states = "my ally states"
    create_enemies = "create enemies"
    my_enemy_states = "my enemy states"
    my_skill_states = "my skill states"
    current_turn = "current turn"
    turn_log = "turn log"

target_type = Union['c.Character', None]
class UIUpdate():
    def __init__(self, event:CombatUIEvent, payload:Any, target:target_type=None):
        self.event = event
        self.target = target
        self.payload = payload

class UIManager:
    def update(self, updates:List[UIUpdate]):
        for update in updates:
            if update.target:
                sid = identity_manager.get_sid(update.target)
                socketio.emit(update.event.value, update.payload, room=sid, namespace='/test')
            else:
                socketio.emit(update.event.value, update.payload, broadcast=True, namespace='/test')

