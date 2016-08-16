
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

    def undo(self):
        pass


# undo the last skill cast on the target
# Note: all undo commands in events should literally just undo the do
# the assumption is that we've already reverted back to the state at the time of the event
class UndoState(Event):
    def __init__(self, caster, target):
        super().__init__(caster, target)

    def do(self):
        self.last_affected_update = self.target.get_last_affected_update
        self.last_affected_update.undo()

    def undo(self):
        self.last_affected_update.do()


# target is who the conditional goes onto
class AddConditional(Event):
    def __init__(self, caster, target, conditional, pre):
        super().__init__(caster, None)
        self.conditional = conditional
        self.pre = pre

    def do(self):
        self.target.add_status(self.conditional)

    def undo(self):
        self.target.remove_status(self.conditional)


class Damage(Event):
    def __init__(self, caster, target, damage):
        super().__init__(caster, target)
        self.damage = damage

    def do(self):
        self.target.health = self.target.health - (self.damage - self.target.defense)

    def undo(self):
        self.target.health = self.target.health + (self.damage - self.target.defense)

    def set_damage(self, amount):
        if amount < 0:
            self.damage = 0
        else:
            self.damage = amount


class Heal(Event):
    def __init__(self, caster, target, heal):
        super().__init__(caster, target)
        self.heal = heal

    def do(self):
        self.target.health = self.target.health + self.heal

    def undo(self):
        self.target.health = self.target.health + self.heal


class ApplyStatus(Event):
    def __init__(self, caster, target, status_effect):
        super().__init__(caster, target)
        self.status_effect = status_effect

    def do(self):
        self.target.add_status_effects(self.status_effect)

    def undo(self):
        self.target.undo_status_effects(self.status_effect)


class ReduceMana(Event):
    def __init__(self, caster, target, mana):
        super().__init__(caster, target)
        self.mana = mana

    def do(self):
        self.target.mana = self.target.mana - self.mana

    def undo(self):
        self.target.mana = self.target.mana + self.mana


class SkillCast:
    def __init__(self, caster, target, skill, events:List[Event]):
        self.caster = caster
        self.target = target
        self.skill = skill
        self.events = events

    def change_target(self, old_target, new_target):
        for event in self.events:
            if event.target == old_target:
                event.target = new_target

            # else it's an AoE
            if self.target == old_target:
                self.target = new_target

    def do(self):
        for event in self.events:
            event.do()


# TODO:abstract this out to deal with AoE
class SingleHealCast(SkillCast):
    def __init__(self, caster, target, skill, events):
        super().__init__(caster, target, skill, events)

    def get_heal_amount(self):
        for event in self.events:
            if event.__class__ == Heal:
                return event.heal
        else:
            return 0
