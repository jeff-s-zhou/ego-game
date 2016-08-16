from typing import Tuple, List

import combat
from status import Status

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


class Conditional(Status):
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


PreConditionalReturnType = Tuple(combat.SkillCast, List[combat.SkillCast])

class PreConditional(Conditional):
    def __init__(self, caster, target, types, state_handler):
        super().__init__(caster, target, types, state_handler)

    def modify(self, cast: combat.SkillCast) -> PreConditionalReturnType:
        pass


class PostConditional(Conditional):
    def __init__(self, caster, target, types, state_handler):
        super().__init__(caster, target, types, state_handler)

    def modify(self, cast: combat.SkillCast) -> List[combat.SkillCast]:
        pass


class Protect(PreConditional):
    def __init__(self, caster, target):
        state_handler = Temporary(2)
        super().__init__(caster, target, [combat.Type.holy], state_handler)

    def modify(self, cast):
        if (cast.target == self.target):
            cast.set_target(self.target, self.caster)
            self.state_handler.triggered()
            return cast, None


class Lifesteal(PostConditional):
    def __init__(self, caster):
        self.caster = caster
        state_handler = Permanent(6)
        super().__init__(caster, caster, [combat.Type.lifesteal], state_handler)

    def modify(self, cast):
        if cast.caster == self.caster and cast.damage > 0:
            self.state_handler.triggered()
            return self.cast_active(cast)
        else:
            return None

    def cast_active(self, original_cast:combat.SkillCast) -> combat.SkillCast:
        heal = combat.Heal(self.caster, self.caster, original_cast.damage / 25)
        return combat.SingleHealCast(self.caster, original_cast.target, self, [heal])


class BlackBlood(PreConditional):
    def __init__(self, caster):
        self.caster = caster
        self.valid = True
        state_handler = Temporary(4)
        super().__init__(caster, caster, [], state_handler)

    def modify(self, cast):
        if cast.target == self.caster and cast.skill.has_type(combat.Type.lifesteal):
            self.state_handler.triggered()
            return cast, self.cast_active(cast)
        else:
            return cast, None

    def cast_active(self, original_cast:combat.SingleHealCast) -> combat.SkillCast:
        heal_amount = original_cast.get_heal_amount()
        damage = combat.Damage(original_cast.target, original_cast.caster, heal_amount)
        return combat.SkillCast(original_cast.target, original_cast.caster, self, [damage])
