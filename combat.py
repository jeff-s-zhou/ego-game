
# get the role of the current player #
from enum import Enum
import character as c
import active_skills as s
import status_effects
from typing import List, Dict, Union

class Type(Enum):
    fire = 1
    holy = 2
    lifesteal = 3


class ActionType(Enum):
    damage = "damage"
    add_status = "add_status"
    heal = "heal"
    remove_status = "remove_status"
    reduce_mp = "reduce_mp"
    add_conditional = "add_conditional"


action_value_type = Union[int, "status_effects.StatusEffect"]
class Action:
    def __init__(self, a_type: ActionType, value:action_value_type):
        self.a_type = a_type
        self.value = value


class Cast:
    def __init__(self, caster:'c.Character',
                 targets: List['c.Character'],
                 explicit_targets : List['c.Character'],
                 skill: 's.Skill',
                 payloads: Dict[int, List[Action]]):
        self.caster = caster
        self.skill = skill
        self.targets = targets
        self.explicit_targets = explicit_targets #for writing into the combat log in the pre cast
        self.payloads = payloads # can include caster if there is a payload for the caster
        self.modifier_messages = []


class SkillCast(Cast):
    def __init__(self, caster, targets, explicit_targets, skill, payloads):
        super().__init__(caster, targets, explicit_targets, skill, payloads)
        self.base_description = ""
        self.set_base_description()

    def set_base_description(self):
        caster_name = self.caster.name
        target_names = ", ".join([target.name for target in self.explicit_targets])
        verb = self.skill.verb
        skill_name = self.skill.name
        self.base_description = "{0} {1} {2} with {3}. ".format(caster_name, verb, target_names, skill_name)

    def description(self):
        modifier_messages = "".join(self.modifier_messages)
        return self.base_description + modifier_messages

    def add_payload_for(self, payload, target, explicit=True):
        self.payloads[target.id] = payload
        self.targets.append(target)
        if(explicit):
            self.explicit_targets.append(target)

    def remove_payload_for(self, target, explicit=True):
        old_payload = self.payloads[target.id]
        del self.payloads[target.id]
        self.targets.remove(target)
        if(explicit):
            self.explicit_targets.remove(target)
        return old_payload


class ReactionCast(Cast):
    def __init__(self, caster, targets, explicit_targets, skill, payloads, shortform):
        super().__init__(caster, targets, explicit_targets, skill, payloads)
        self.shortform = shortform


