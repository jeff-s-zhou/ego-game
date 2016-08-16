import conditionals

import combat


class PassiveSkill():
    def __init__(self, caster, max_cooldown):
        self.caster = caster

    # passive skills are all "cast" at the start of battle
    # and whenever their cooldowns are off
    def cast(self):
        pass

# this is basically an active skill, except applied when another skill triggers it
class Lifesteal(PassiveSkill):
    def __init__(self, caster):
        super().__init__(caster)

    def cast(self):
        lifesteal = conditionals.Lifesteal(self.caster)
        conditional_event = combat.AddConditional(self.caster, self.caster, lifesteal, pre=False)
        return combat.SkillCast(self.caster, self.caster, self, [conditional_event])
