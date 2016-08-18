from collections import defaultdict
from typing import List

from character import Character
from combat import SkillCast

class CombatManager:
    def __init__(self, combatants):
        self.combatants = combatants
        self.current_combatant_index = 0
        self.global_pre_conditional_listeners = []
        self.global_post_conditional_listeners = []
        # apply passives

    #get the precombat state from the perspective of the character
    #that means basic states of everyone, detailed state of yourself
    def get_state_for(self, combatant) -> dict:
        return combatant.get_state()

    #get overall combat state, basic
    def get_state(self) -> List[dict]:
        return [combatant.get_basic_state() for combatant in self.combatants]

    def get_current_combatant(self) -> Character:
        return self.combatants[self.current_combatant_index]

    def resolve_round(self):
        #TODO: make sure it's sorting the right way, resolve tiebreaks fairly

        self.combatants.sort(key=lambda combatant: combatant.stats.initiative)
        #TODO: find a way to change initiative in the same round

    def turn_time_up(self):
        self.current_combatant_index += 1

    def resolve_turn(self, input):
        caster = self.get_current_combatant()
        caster.my_turn_start()

        target, skill = self.lookup_input(input)
        skill_cast = self.get_current_combatant().casts(skill, target)
        self.resolve_cast(skill_cast)
        # TODO: I need to figure out where I return the message log

        # TODO: remove invalids actors
        self.current_combatant_index += 1

    def lookup_input(self, turn_input):
        caster_name = turn_input['caster_name']
        skill_name = turn_input['skill_name']
        target_name = turn_input['target_name']
        target = None
        caster = None
        for combatant in self.combatants:
            if combatant.name == caster_name:
                caster = combatant

            if combatant.name == target_name:
                target = combatant

        selected_skill = None
        for skill in caster.active_skills:
            if skill.name == skill_name:
                selected_skill = skill

        return selected_skill, target


    def resolve_cast(self, skill_cast):
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