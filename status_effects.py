from enum import Enum
from typing import Tuple, List

import combat

class StateHandler():
    def __init__(self):
        self.valid = True

    def triggered(self):
        pass

    def turn_tick(self):
        pass

    def is_castable(self):
        pass


class Permanent(StateHandler):
    def __init__(self, max_cooldown):
        self.max_cooldown = max_cooldown
        self.cooldown = 0
        super().__init__()

    def triggered(self):
        self.cooldown = self.max_cooldown

    def turn_tick(self):
        if self.cooldown > 0:
            self.cooldown -= self.cooldown

    def is_castable(self):
        return self.cooldown == 0


class Temporary(StateHandler):
    def __init__(self, duration):
        self.duration = duration
        super().__init__()

    def triggered(self):
        self.valid = False

    def turn_tick(self):
        self.duration -= 1
        if self.duration == 0:
            self.valid = False

    def is_castable(self):
        return self.valid


class StatusEffect:
    def __init__(self):
        pass

    def is_valid(self):
        return False

    def is_visible(self):
        return False

    # TODO
    def to_dict(self):
        return None

    def applied_to_string(self):
        return ''


class ConditionalType(Enum):
    pre = "pre"
    post = "post"
    self = "self"
    others = "others"

class Conditional(StatusEffect):
    def __init__(self, caster, target, types, state_handler:StateHandler):
        super().__init__()
        self.caster = caster
        self.target = target
        self.types = types
        self.state_handler = state_handler

    def has_type(self, type):
        return type in self.types

    def is_valid(self):
        return self.state_handler.valid

    def is_castable(self):
        return self.state_handler.is_castable()


class Protected(Conditional):
    def __init__(self, caster, target):
        state_handler = Temporary(2)
        super().__init__(caster, target, [ConditionalType.pre, ConditionalType.self], state_handler)

    def react_to(self, cast):
            #replace cast target with caster of buff
            old_payload = cast.remove_payload_for(self.target)
            cast.add_payload_for(old_payload, self.caster)

            modifier_message = "{0} is protecting {1}! ".format(self.caster.name, self.target.name)
            cast.modifier_messages.append(modifier_message)
            self.state_handler.triggered()
            return None

    def applied_to_string(self):
        return 'Protected'

class ThornBound(Conditional):
    def __init__(self, caster, target):
        state_handler = Temporary(2)
        super().__init__(caster, target, [ConditionalType.post, ConditionalType.self], state_handler)
        self.procs = 5

    def react_to(self, state_update):
            if state_update.new_state.hp >= state_update.old_state.hp:
                return None

            #else took damage
            damage_event = combat.Event(combat.EventType.damage, 100)
            payloads = {self.target.id: [damage_event]}
            thorn_bound_reaction = combat.ReactionCast(self.caster, [self.target],
                                                       [self.target], self, payloads, "Thorn Bound")
            self.procs -= 1
            if(self.procs == 0):
                self.state_handler.triggered()
            print("returning thorn_bound_reaction")
            return thorn_bound_reaction

    def applied_to_string(self):
        return 'Thorn Bound'
