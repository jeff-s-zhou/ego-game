import status_effects

import combat

import character as ch

import constants


class Skill:
    def __init__(self, skill_constant: constants.SKILL_CONSTANT, caster: 'ch.Character'):
        self.id = skill_constant.id
        self.name = skill_constant.name
        self.description = skill_constant.tooltip
        self.verb = skill_constant.verb
        self.valid_targets = skill_constant.valid_targets

        self.caster = caster

    def cast(self, target: 'ch.Character') -> 'combat.SkillCast':
        pass

    def has_type(self, type):
        return None

    def to_dict(self):
        pass

    def turn_tick(self):
        pass


# we're choosing not to do a big tree of inheritance because each skill should feel pretty unique

# single target prototype
class Slash(Skill):
    def __init__(self, caster: 'ch.Character'):
        super().__init__(constants.SLASH, caster)
        self.cooldown = 0
        self.damage = constants.SLASH.damage_multiplier * caster.stats.damage

    def cast(self, target):
        # TODO: check if target(s) are valid
        self.cooldown = constants.SLASH.cooldown
        damage = combat.Action(combat.ActionType.damage, self.damage)
        mana_cost = combat.Action(combat.ActionType.reduce_mp, constants.SLASH.balance_cost)
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
        super().__init__(constants.HEAL, caster)
        self.cooldown = 0
        self.heal_amount = constants.HEAL.heal_amount

    def cast(self, target):
        self.cooldown = constants.HEAL.cooldown
        heal = combat.Action(combat.ActionType.heal, self.heal_amount)
        mana_cost = combat.Action(combat.ActionType.reduce_mp, constants.HEAL.balance_cost)
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
        super().__init__(constants.PROTECT, caster)

    def cast(self, target):
        self.cooldown = constants.PROTECT.cooldown
        protect_buff = status_effects.Protected(self.caster, target)
        buff_action = combat.Action(combat.ActionType.add_conditional, protect_buff)
        mana_cost = combat.Action(combat.ActionType.reduce_mp, constants.PROTECT.balance_cost)
        payloads = {target.id: [buff_action], self.caster.id: [mana_cost]}
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
        super().__init__(constants.ELECTRIC_THORN_BIND, caster)

    def cast(self, target):
        self.cooldown = constants.ELECTRIC_THORN_BIND.cooldown
        thorn_bound = status_effects.ThornBound(self.caster, target)
        debuff_action = combat.Action(combat.ActionType.add_conditional, thorn_bound)
        mana_cost = combat.Action(combat.ActionType.reduce_mp, constants.ELECTRIC_THORN_BIND.balance_cost)
        payloads = {target.id: [debuff_action], self.caster.id: [mana_cost]}
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
