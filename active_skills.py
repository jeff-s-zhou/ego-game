from enum import Enum

import status

#CONSTANTS

#slash
SLASH_DAMAGE_MULTIPLIER = 20
SLASH_COOLDOWN = 1
SLASH_TOOLTIP = ""
SLASH_MANA_COST = 10

#fireball
FIREBALL_DAMAGE_MULTIPLIER = 10
FIREBALL_COOLDOWN = 6
FIREBALL_TOOLTIP = ""

#valid targets
#...do we just want to make this really mathy and then spit out the names?
#like, for all allies we do all - all_targets?
class Targets(Enum):
    self = 0
    single_enemy = 1
    enemy_frontline = 2
    enemy_backline = 3
    all_enemies = 4
    single_ally = 5
    ally_frontline = 6
    ally_backline = 7
    all_allies = 8
    all = 9



class Event:
    def __init__(self, caster, target_name):
        #TODO: we want an author on all events
        self.author = None
        self.caster = caster
        self.target_name = target_name


#undo the last skill cast on the target
class UndoState(Event):
    def __init__(self, caster, target_name):
        super().__init__(caster, target_name)

    def do(self, target):
        self.last_affected_update = target.get_last_affected_update
        self.last_affected_update.undo()

    def undo(self, target):
        self.last_affected_update.do()

class Damage(Event):
    def __init__(self, caster, target_name, damage):
        super().__init__(caster, target_name)
        self.damage = damage

    def do(self, target):
        target.health = target.health - (self.damage - target.defense)

    def undo(self, target):
        target.health = target.health + (self.damage - target.defense)

class ApplyStatus(Event):
    def __init__(self, caster, target_name, status_effect):
        super().__init__(caster, target_name)
        self.status_effect = status_effect

    def do(self, target):
        target.add_status_effects(self.status_effect)

    def undo(self, target):
        target.undo_status_effects(self.status_effect)


class ReduceMana(Event):
    def __init__(self, caster, target_name, mana):
        super().__init__(caster, target_name)
        self.mana = mana

    def do(self, target):
        target.mana = target.mana - self.mana

    def undo(self, target):
        target.mana = target.mana + self.mana



class Skill:
    def __init__(self, caster):
        self.caster = caster

    def cast(self, target_name, others):
        pass

#we're choosing not to do a big tree of inheritance because each skill should feel pretty unique

#each player has one Skill for each skill they have
#single target prototype
class Slash(Skill):
    def __init__(self, caster):
        super().__init__(caster)
        self.cooldown = 0
        self.damage = SLASH_DAMAGE_MULTIPLIER * caster.damage
        self.valid_targets = [Targets.single_enemy]

    def cast(self, target_name, other_names):
        self.cooldown = 6
        damage = Damage(self.caster, target_name, self.damage),
        mana_cost = ReduceMana(self.caster, self.caster, SLASH_MANA_COST)
        return [damage, mana_cost]

#aoe prototype
class Fireball(Skill):
    def __init__(self, caster):
        super().__init__(caster)
        self.damage = FIREBALL_DAMAGE_MULTIPLIER * caster.damage
        self.valid_targets = [Targets.single_enemy, Targets.enemy_backline,
                              Targets.enemy_frontline, Targets.all_enemies]

    def cast(self, target_name, other_names):
        #TODO: overloading on equals
        if target_name == Targets.single_enemy:
            pass
        elif target_name == Targets.all_enemies:
            pass

#single target dot prototype
class Poison(Skill):
    def __init__(self, caster):
        super().__init__(caster)

    def cast(self, target_name, other_names):
        pass

#trap prototype
class FreezeTrap(Skill):
    def __init__(self):
        super().__init__()

#counter prototype
class Riposte(Skill):
    def __init__(self):
        super().__init__()

#heal prototype
class Prayer(Skill):
    def __init__(self):
        super().__init__()

#focus prototype
class Snipe(Skill):
    def __init__(self):
        super().__init__()

#channel prototype
class Meteor(Skill):
    def __init__(self):
        super().__init__()

class LightsLitany(Skill):
    def __init__(self, caster, target):
        super().__init__()

#only allowed target is ALL
class FinalJudgment(Skill):
    def __init__(self, caster, target):
        super().__init__()
