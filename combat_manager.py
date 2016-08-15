from collections import defaultdict

from character import Character
from combat import SkillCast


class CombatManager:
    def __init__(self, combatants):
        self.combatants = combatants
        self.global_pre_conditional_listeners = []
        self.global_post_conditional_listeners = []
        # apply passives

    def get_precombat_state(self):
        return None

    def resolve_round(self):
        # signal top of round tick
        # for combatant in ordered_combatants:
        # self.resolve_turn(combatant)
        # signal end of round tick
        # remove invalids
        pass

    def resolve_turn(self, combatant:Character):
        combatant.my_turn_start()

        # caster, target, skill_cast = wait 5 seconds for command by combatant
        # skill_cast = character.casts(skill, target)?
        # self.resolve_cast(caster, target, skill_cast)
        # TODO: I need to figure out where I return the message log

        # signal turn tick
        # remove invalids

        # return updated state of all characters? or just characters affected? let's just do all for now
        return None

    def resolve_cast(self, caster, target, skill_cast):
        casts = [skill_cast]
        while casts:
            # handle pre cast conditionals
            current_cast = casts.pop()
            modified_cast, new_casts = self.apply_pre_conditionals(current_cast)
            casts.append(new_casts)

            modified_cast.do()

            # handle post cast conditionals
            new_casts = self.apply_post_conditionals(modified_cast)
            casts.append(new_casts)

    def apply_pre_conditionals(self, cast:SkillCast):
        valid_listeners = self.get_pre_listeners(cast)

        modified_cast = cast
        new_casts = []
        for listener in valid_listeners:
            new_modified, new_cast = listener.modify(cast)
            modified_cast = new_modified
            new_casts.append(new_cast)

        return modified_cast, new_casts

    def get_pre_listeners(self, cast):
        return cast.caster.get_pre_listeners + \
               cast.target.get_pre_listeners + self.global_pre_conditional_listeners

    def apply_post_conditionals(self, cast):
        affected = cast.get_affected_units
        valid_listeners = self.get_post_listeners(affected)

        new_casts = []
        for listener in valid_listeners:
            new_cast = listener.modify(cast)
            new_casts.append(new_cast)

        return new_casts

    def get_post_listeners(self, cast):
        return cast.caster.get_post_listeners + \
               cast.target.get_post_listeners + self.global_post_conditional_listeners

    def add_global_pre_listener(self, listener):
        self.global_pre_conditional_listeners.append(listener)

    def add_global_post_listener(self, listener):
        self.global_post_conditional_listeners.append(listener)