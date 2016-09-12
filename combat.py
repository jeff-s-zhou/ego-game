
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
    def __init__(self, type, value):
        self.type = type
        self.value = value


class EventType(Enum):
    damage = 1
    add_status = 2
    heal = 3
    remove_status = 4
    reduce_mp = 5
    add_conditional = 6


class SkillCast:
    def __init__(self, caster, targets, explicit_targets, skill, payloads):
        self.caster = caster
        self.skill = skill
        self.targets = targets
        self.explicit_targets = explicit_targets #for writing into the combat log in the pre cast
        self.payloads = payloads # can include caster if there is a payload for the caster

    def description(self):
        caster_name = self.caster.name
        target_names = ", ".join([target.name for target in self.explicit_targets])
        verb = self.skill.verb
        skill_name = self.skill.name
        return "{0} {1} {2} with {3}.".format(caster_name, verb, target_names, skill_name)

class Reaction(SkillCast):
    def __init__(self, caster, targets, explicit_targets, skill, payloads, shortform):
        super().__init__(caster, targets, explicit_targets, skill, payloads)
        self.shortform = shortform


