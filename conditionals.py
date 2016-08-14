import combat

class Conditional():
    def __init__(self, affected, types):
        self.affected = affected
        self.types = types

    def hasType(self, type):
        return type in self.types


# postconditional, temporary
class Protect(Conditional):
    def __init__(self, caster, target):
        self.priority = 1
        self.valid = True
        self.duration = 1
        self.caster = caster
        self.target = target
        self.permanent = False
        super().__init__([target], [combat.Type.holy])

    def modify(self, cast):
        if (cast.target == self.target):
            cast.set_target(self.target, self.caster)
            self.triggered()
            return cast, None

    def triggered(self):
        self.valid = False

    def caster_turn_round_tick(self):
        self.duration -= 1
        if self.duration == 0:
            self.valid = False


# postconditional, permanent
class Lifesteal(Conditional):
    def __init__(self, caster):
        self.priority = 1
        self.cooldown = 0
        self.caster = caster
        self.valid = True
        self.permanent = True
        super().__init__([caster], combat.Type.lifesteal)

    def modify(self, cast):
        if cast.caster == self.caster and cast.damage > 0 and self.valid == True:
            self.triggered()
            #TODO: refactor this into calling the LifestealActive.do()?
            return self.cast_active(cast)

    def triggered(self):
        self.valid = False
        self.cooldown = 6

    def caster_turn_round_tick(self):
        if self.valid == False:
            self.cooldown -= 1
            if (self.cooldown == 0):
                self.valid = True

    def cast_active(self, cast):
        #TODO: might need to change the self call to the original passive
        heal = combat.Heal(self.caster, self.caster, cast.damage / 25)
        return combat.SingleHealCast(self.caster, cast.target, self, [heal])


# preconditional, temporary
class BlackBlood(Conditional):
    def __init__(self, caster):
        self.priority = 1
        self.caster = caster
        self.duration = 5
        self.valid = True
        super().__init__([caster], [])

    def modify(self, cast):
        if cast.target == self.caster and cast.skill.hasType(combat.Type.lifesteal):
            self.triggered()
            return self.cast_active(cast)

    def triggered(self):
        self.valid = False

    def caster_turn_round_tick(self):
        self.duration -= 1
        if self.duration == 0:
            self.valid = False

    def cast_active(self, cast):
            heal_amount = cast.get_heal_amount()
            damage = combat.Damage(cast.target, cast.caster, heal_amount)
            return combat.SkillCast(cast.target, cast.caster, self, [damage])