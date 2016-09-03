
# get the role of the current player #
from enum import Enum

from typing import List

class Type(Enum):
    fire = 1
    holy = 2
    lifesteal = 3


'''we use the command pattern here instead of functional programming
because each event needs an author so we can undo all of them that belong to the same skill.
We also want the round and turn it's cast on so we can undo everything from a specific time
'''

class Event:
    def __init__(self, caster, target):
        # TODO: we want an author on all events
        self.author = None
        # TODO: also want the round and turn it's cast on
        self.round = None
        self.turn = None
        self.caster = caster
        self.target = target

    def do(self):
        pass


class Damage(Event):
    def __init__(self, caster, target, damage):
        super().__init__(caster, target)
        self.damage = damage

    def do(self):
        return self.target.take_damage(self.damage)

class ApplyStatus(Event):
    def __init__(self, caster, target, status_effect):
        super().__init__(caster, target)
        self.status_effect = status_effect

    def do(self):
        return self.target.add_status_effects(self.status_effect)


class ReduceMp(Event):
    def __init__(self, caster, target, mp):
        super().__init__(caster, target)
        self.mp = mp

    def do(self):
        return self.target.reduce_mp(self.mp)


#single target, multiple effects
class Payload:
    def __init__(self, events):
        self.events = events

    def deliver(self):
        reactions = []
        status_updates = []
        for event in self.events:
            reaction, status_update = event.do()
            reactions.append(reaction)
            status_updates.append(status_update)
        return reactions, status_updates

    def get_target(self):
        return self.events[0].target

class SkillCast:
    def __init__(self, caster, targets, skill, payloads):
        self.caster = caster
        self.skill = skill
        self.targets = targets
        self.payloads = payloads # can include caster if there is a payload for the caster



