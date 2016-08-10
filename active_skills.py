from enum import Enum

#CONSTANTS

#slash
SLASH_DAMAGE_MULTIPLIER = 20

#fireball
FIREBALL_DAMAGE_MULTIPLIER = 10


#Combat skills

class Properties(Enum):
    line_aoe = 1
    party_aoe = 2
    heal = 3


class Skill:
    def __init__(self):
        pass

    def activate(self, caster, target, others):
        pass


#we're choosing not to do a big tree of inheritance because each skill should feel pretty unique

class Slash(Skill):
    def __init__(self, caster):
        self.properties = []
        self.damage = SLASH_DAMAGE_MULTIPLIER * caster.attack
        self.on_hit_effects = caster.on_hit_effects
        super().__init__()

    def activate(self, caster, target, others):
        target.damage(self.damage)
        super().activate(caster, target, others)

class Fireball(Skill):
    def __init__(self, caster):
        self.properties = [Properties.line_aoe]
        self.damage = FIREBALL_DAMAGE_MULTIPLIER * caster.attack
        self.on_hit_effects = caster.on_hit_effects
        super().__init__()

    def activate(self, caster, target, others):
        target.damage(self.damage)
        super().activate(caster, target, others)


class Poison(Skill):
    def __init__(self):
        super().__init__()

    def activate(self, caster, target, others):
        #target.debuff(poison_debuff)
        super().activate(caster, target, others)

#hearthstone's secrets
class Trap(Skill):
    def __init__(self):
        super().__init__()

#like secrets, but not hidden
class Riposte(Skill):
    def __init__(self):
        super().__init__()

class LightsLitany(Skill):
    def __init__(self, caster, target):
        super().__init__()

#only allowed target is ALL
class FinalJudgment(Skill):
    def __init__(self, caster, target):
        super().__init__()
