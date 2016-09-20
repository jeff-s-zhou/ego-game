from enum import Enum

import status_effects

import combat

import character as ch

# CONSTANTS

# slash
SLASH_DAMAGE_MULTIPLIER = 50
SLASH_COOLDOWN = 1
SLASH_TOOLTIP = ""
SLASH_MANA_COST = 10

# fireball
FIREBALL_DAMAGE_MULTIPLIER = 10
FIREBALL_COOLDOWN = 6
FIREBALL_TOOLTIP = ""

# protect
PROTECT_COOLDOWN = 4
PROTECT_MANA_COST = 30

# heal
HEAL_AMOUNT = 90
HEAL_COOLDOWN = 3
HEAL_MANA_COST = 20

#thorn bind hostage
THORN_BIND_HOSTAGE_COOLDOWN = 5
THORN_BIND_HOSTAGE_MANA_COST = 30


# valid allies
# ...do we just want to make this really mathy and then spit out the names?
# like, for all allies we do all - all_targets?
class Targets(Enum):
    self = 'self'
    single_enemy = 'single_enemy'
    enemy_frontline = 'enemy_frontline'
    enemy_backline = 'enemy_backline'
    all_enemies = 'all_enemies'
    single_ally = 'single_ally'
    ally_frontline = 'ally_frontline'
    ally_backline = 'ally_backline'
    all_allies = 'all_allies'
    all = 'all'


class Skill:
    def __init__(self, id:int, name:str, description:str, caster: 'ch.Character', types, valid_targets, verb:str):
        self.id = id
        self.name = name
        self.description = description
        self.caster = caster
        self.types = types
        self.verb = verb
        self.valid_targets = valid_targets

    def cast(self, target: 'ch.Character') -> 'combat.SkillCast':
        pass

    def has_type(self, type):
        return type in self.types

    def to_dict(self):
        pass

    def turn_tick(self):
        pass



# we're choosing not to do a big tree of inheritance because each skill should feel pretty unique

# single target prototype
class Slash(Skill):
    def __init__(self, caster: 'ch.Character'):
        super().__init__(1, 'Slash', 'A cutting skill.',  caster, [], [Targets.single_enemy], 'attacks')
        self.cooldown = 0
        self.damage = SLASH_DAMAGE_MULTIPLIER * caster.stats.damage

    def cast(self, target):
        # TODO: check if target(s) are valid
        self.cooldown = SLASH_COOLDOWN
        damage = combat.Event(combat.EventType.damage, self.damage)
        mana_cost = combat.Event(combat.EventType.reduce_mp, SLASH_MANA_COST)
        payloads = {target.id: [damage], self.caster.id: [mana_cost]}
        return combat.SkillCast(self.caster, [target, self.caster], [target], self, payloads)

    def turn_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def is_valid(self):
        return self.cooldown == 0

    def to_dict(self):
        valid_targets = [target.value for target in self.valid_targets]
        return {
            'id': self.id, 'name': self.name,
            'description': self.description,
            'condition': self.cooldown,
            'valid': self.is_valid(),
            'valid_targets': valid_targets
        }


class Heal(Skill):
    def __init__(self, caster: 'ch.Character'):
        super().__init__(2, 'Heal', 'A healing spell.', caster, [], [Targets.single_ally], 'heals')
        self.cooldown = 0
        self.heal_amount = HEAL_AMOUNT

    def cast(self, target):
        self.cooldown = HEAL_COOLDOWN
        heal = combat.Event(combat.EventType.heal, self.heal_amount)
        mana_cost = combat.Event(combat.EventType.reduce_mp, HEAL_MANA_COST)
        payloads = {target.id: [heal], self.caster.id: [mana_cost]}
        return combat.SkillCast(self.caster, [target, self.caster], [target], self, payloads)

    def turn_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def is_valid(self):
        return self.cooldown == 0

    def to_dict(self):
        valid_targets = [target.value for target in self.valid_targets]
        return {
            'id': self.id, 'name': self.name,
            'description': self.description,
            'condition': self.cooldown,
            'valid': self.is_valid(),
            'valid_targets': valid_targets
        }


# targetable buff prototype
class Protect(Skill):
    def __init__(self, caster):
        self.cooldown = 0
        super().__init__(3, 'Protect', 'Take damage for the target for 3 turns.',
                         caster, [], [Targets.single_ally], "supports")

    def cast(self, target):
        self.cooldown = PROTECT_COOLDOWN
        protect_buff = status_effects.Protected(self.caster, target)
        buff_event = combat.Event(combat.EventType.add_conditional, protect_buff)
        mana_cost = combat.Event(combat.EventType.reduce_mp, PROTECT_MANA_COST)
        payloads = {target.id: [buff_event], self.caster.id: [mana_cost]}
        return combat.SkillCast(self.caster, [target, self.caster], [target], self, payloads)

    def turn_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def is_valid(self):
        return self.cooldown == 0

    def to_dict(self):
        valid_targets = [target.value for target in self.valid_targets]
        return {
            'id': self.id, 'name': self.name,
            'description': self.description,
            'condition': self.cooldown,
            'valid': self.is_valid(),
            'valid_targets': valid_targets
        }


class ThornBindHostage(Skill):
    def __init__(self, caster):
        self.cooldown = 0
        super().__init__(3, 'Thorn Bind Hostage', 'Cast Thorn Bound on target.',
                         caster, [], [Targets.single_enemy], "curses")

    def cast(self, target):
        self.cooldown = THORN_BIND_HOSTAGE_COOLDOWN
        thorn_bound = status_effects.ThornBound(self.caster, target)
        debuff_event = combat.Event(combat.EventType.add_conditional, thorn_bound)
        mana_cost = combat.Event(combat.EventType.reduce_mp, THORN_BIND_HOSTAGE_MANA_COST)
        payloads = {target.id: [debuff_event], self.caster.id: [mana_cost]}
        return combat.SkillCast(self.caster, [target, self.caster], [target], self, payloads)

    def turn_tick(self):
        if self.cooldown > 0:
            self.cooldown -= 1

    def is_valid(self):
        return self.cooldown == 0

    def to_dict(self):
        valid_targets = [target.value for target in self.valid_targets]
        return {
            'id': self.id, 'name': self.name,
            'description': self.description,
            'condition': self.cooldown,
            'valid': self.is_valid(),
            'valid_targets': valid_targets
        }

'''
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
        super().__init__()'''
