

#damage to the target, health to the caster

#this is basically an active skill, except applied when another skill triggers it
class Lifesteal:
    def __init__(self, caster):
        self.damage = 5 * caster.attack

    def do(self, caster, target, others):
        pass

    def undo(self, caster, target, others):
        pass