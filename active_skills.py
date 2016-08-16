from enum import Enum

import status

import combat

import conditionals

from character import Character

# CONSTANTS

# slash
SLASH_DAMAGE_MULTIPLIER = 20
SLASH_COOLDOWN = 1
SLASH_TOOLTIP = ""
SLASH_MANA_COST = 10

# fireball
FIREBALL_DAMAGE_MULTIPLIER = 10
FIREBALL_COOLDOWN = 6
FIREBALL_TOOLTIP = ""

# protect
PROTECT_COOLDOWN = 4


# valid targets
# ...do we just want to make this really mathy and then spit out the names?
# like, for all allies we do all - all_targets?
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


class Skill:
    def __init__(self, caster: Character, types):
        self.caster = caster
        self.types = types

    def cast(self, target: Character) -> combat.SkillCast:
        pass

    def has_type(self, type):
        return type in self.types




# we're choosing not to do a big tree of inheritance because each skill should feel pretty unique

# single target prototype
class Slash(Skill):
    def __init__(self, caster):
        super().__init__(caster, [])
        self.cooldown = 0
        self.damage = SLASH_DAMAGE_MULTIPLIER * caster.damage
        self.valid_targets = [Targets.single_enemy]

    def cast(self, target):
        # TODO: check if target is valid?
        self.cooldown = SLASH_COOLDOWN
        damage = combat.Damage(self.caster, target, self.damage),
        mana_cost = combat.ReduceMana(self.caster, self.caster, SLASH_MANA_COST)
        return combat.SkillCast(self.caster, target, self, [damage, mana_cost])


# targetable buff prototype
class Protect(Skill):
    def __init__(self, caster):
        self.cooldown = 0
        super().__init__(caster, [combat.Type.holy])
        self.valid_targets = [Targets.single_ally]

    def cast(self, target):
        self.cooldown = PROTECT_COOLDOWN
        conditional_event = combat.AddConditional(self.caster, self.target, conditionals.Protect(self.caster, target),
                                                  True)
        return combat.SkillCast(self.caster, target, self, [conditional_event])


# aoe prototype
class Fireball(Skill):
    def __init__(self, caster):
        super().__init__(caster, [])
        self.damage = FIREBALL_DAMAGE_MULTIPLIER * caster.damage
        self.valid_targets = [Targets.single_enemy, Targets.enemy_backline,
                              Targets.enemy_frontline, Targets.all_enemies]

    def cast(self, target):
        # TODO: overloading on equals
        if target == Targets.single_enemy:
            pass
        elif target == Targets.all_enemies:
            pass


# single target dot prototype
class Poison(Skill):
    def __init__(self, caster):
        super().__init__(caster, [])

    def cast(self, target):
        pass


# trap prototype
class FreezeTrap(Skill):
    def __init__(self):
        super().__init__()


# counter prototype
class Riposte(Skill):
    def __init__(self):
        super().__init__()


# heal prototype
class Prayer(Skill):
    def __init__(self):
        super().__init__()


# focus prototype
class Snipe(Skill):
    def __init__(self):
        super().__init__()


# channel prototype
class Meteor(Skill):
    def __init__(self):
        super().__init__()


class LightsLitany(Skill):
    def __init__(self, caster, target):
        super().__init__()


# only allowed target is ALL
class FinalJudgment(Skill):
    def __init__(self, caster, target):
        super().__init__()
