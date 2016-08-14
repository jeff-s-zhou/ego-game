
#get the role of the current player #
from enum import Enum


def get_precombat_state(player_count):
    pass



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
        #TODO: we want an author on all events
        self.author = None
        #TODO: also want the round and turn it's cast on
        self.round = None
        self.turn = None
        self.caster = caster
        self.target = target


#undo the last skill cast on the target
class UndoState(Event):
    def __init__(self, caster, target):
        super().__init__(caster, target)

    def do(self):
        self.last_affected_update = self.target.get_last_affected_update
        self.last_affected_update.undo()

    def undo(self):
        self.last_affected_update.do()


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


class SkillCast():
    def __init__(self, caster, target, skill, events):
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


#TODO:, abstract this out to deal with AoE
class SingleHealCast(SkillCast):
    def __init__(self, caster, target, skill, events):
        super().__init__(caster, target, skill, events)

    def get_heal_amount(self):
        for event in self.events:
            if event.__class__ == Heal:
                return event.heal
        else:
            return 0

class CombatManager:
    def __init__(self):
        self.pre_conditional_listeners = []
        self.post_conditional_listeners = []

    def resolve_round(self):
        #signal top of round tick
        #for combatant in ordered_combatants:
            #self.resolve_turn(combatant)
        #signal end of round tick
        pass

    def resolve_turn(self, combatant):
        #signal start of round for combatant tick

        #caster, target, skill_cast = wait 5 seconds for command by combatant
        #self.resolve_cast(caster, target, skill_cast)

        #signal turn tick
        pass

    def resolve_cast(self, caster, target, skill_cast):
        casts = [skill_cast]
        while casts != []:
            #handle pre cast conditionals
            current_cast = casts.pop()
            modified_cast, new_casts = self.apply_pre_conditionals(current_cast)
            casts.append(new_casts)

            modified_cast.do()

            #handle post cast conditionals
            new_casts = self.apply_post_conditionals(modified_cast)
            casts.append(new_casts)

    def apply_pre_conditionals(self, cast):
            affected = cast.get_affected_units
            valid_listeners = self.get_valid_pre_listeners(affected)

            modified_cast = cast
            new_casts = []
            for listener in valid_listeners:
                new_modified, new_cast = listener.modify(cast)
                modified_cast = new_modified
                new_casts.append(new_cast)

            return modified_cast, new_casts


    def get_valid_pre_listeners(self, affected):
        pass

    def apply_post_conditionals(self, cast):
        affected = cast.get_affected_units
        valid_listeners = self.get_valid_post_listeners(affected)

        new_casts = []
        for listener in valid_listeners:
            new_cast = listener.modify(cast)
            new_casts.append(new_cast)

        return new_casts

    def get_valid_post_listeners(self, affected):
        pass

