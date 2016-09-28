from enum import Enum

from shared import identity_manager, socketio

from typing import List, Union, Any


class UICombatEvent(Enum):
    my_ally_states = "my ally states"
    create_enemies = "create enemies"
    my_enemy_states = "my enemy states"
    my_skill_states = "my skill states"
    current_turn = "current turn"
    turn_log = "turn log"

class UIEvent(Enum):
    set_event = "set event"
    create_allies = "create allies"

class EventType(Enum):
    combat_event = "combat event"
    static_event = "static event"
    dynamic_event = "dynamic event"

target_type = Union['c.Character', None]

UIEventType = Union[UIEvent, UICombatEvent]

class UIUpdate():
    def __init__(self, event:UIEventType, payload:Any, target:target_type=None, callback=None):
        self.event = event
        self.target = target
        self.payload = payload
        self.callback = callback


class UIManager:
    def update(self, updates:List[UIUpdate]):
        for update in updates:
            if update.target:
                sid = identity_manager.get_sid(update.target)
                socketio.emit(update.event.value, update.payload, room=sid, namespace='/test', callback=update.callback)
            else:
                socketio.emit(update.event.value, update.payload, broadcast=True, namespace='/test', callback=update.callback)

