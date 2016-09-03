import json
from collections import defaultdict
from typing import List

from character import Character
from combat import SkillCast

class CombatManager:
    def __init__(self, combatants, ui_manager, combat_monitor, combat_logger):
        self.combat_logger = combat_logger
        self.combatants = combatants
        for combatant in self.combatants:
            combatant.combat_logger = combat_logger
        self.ui_manager = ui_manager
        self.combat_monitor = combat_monitor
        # TODO: make sure it's sorting the right way, resolve tiebreaks fairly
        self.combatants.sort(key=lambda combatant: combatant.stats.initiative)
        self.current_combatant_index = 0
        self.round_index = 0
        self.global_pre_conditional_listeners = []
        self.global_post_conditional_listeners = []
        # apply passives

    def resolve_round(self):

        #TODO: find a way to change initiative in the same round
        pass

    def get_current_combatant(self):
        return self.combatants[self.current_combatant_index]

    def next_turn(self):
        if self.current_combatant_index + 1 == len(self.combatants):
            self.current_combatant_index = 0
            self.round_index += 1

        else:
            self.current_combatant_index += 1


    def update(self):
        if self.round_index == 0 and self.current_combatant_index == 0:
            self.ui_manager.combat_start()

        caster = self.get_current_combatant()
        caster.my_turn_start()

        turn_input = self.combat_monitor.get_input()
        if turn_input:
            print("handling turn input")
            skill, target = self.lookup_input(turn_input)
            skill_cast = self.get_current_combatant().casts(skill, target)
            self.resolve_cast(skill_cast)

            # TODO: remove invalids actors

        self.call_update()
        self.next_turn()


    def resolve_cast(self, skill_cast):
        self.hint(skill_cast)
        self.do(skill_cast)

    #hint the intent to cast to all targets, and external listeners
    def hint(self, skill_cast):
        interested_combatants =  skill_cast.targets + self.global_pre_conditional_listeners
        for combatant in interested_combatants:

            #give all interested combatants an opportunity to react to a cast about to happen
            pre_reactions = combatant.tweak_cast(skill_cast)
            for pre_reaction in pre_reactions:
                for combatant in pre_reaction.targets:
                    null_reaction, status_updates = pre_reaction.payloads[combatant.id].deliver()
                    self.combat_logger.log_pre_reaction_update(pre_reaction, status_updates)


    def do(self, skill_cast):
        for target in skill_cast.targets:

            # cast the skill, and give combatant an opportunity to react to state changes
            post_reactions, status_updates = skill_cast.payloads[target.id].deliver()
            self.combat_logger.log_payload_update(skill_cast, status_updates)
            for post_reaction in post_reactions:
                for combatant in post_reaction.targets:
                    null_reaction, status_updates = post_reaction.payloads[combatant.id].deliver()
                    self.combat_logger.log_post_reaction_update(post_reaction, status_updates)

            #give other interested combatants an opportunity to react to a combatant's state change
            for post_listener in self.global_post_conditional_listeners:
                global_reactions = post_listener.sniff(status_updates)
                for global_reaction in global_reactions:
                    for combatant in global_reaction.targets:
                        null_reaction, status_updates = global_reaction.payloads[combatant.id].deliver()
                        self.combat_logger.log_post_reaction_update(global_reaction, status_updates)


    def call_update(self):
        for combatant in self.combatants:
            allies_state = [ally.get_ally_state() for ally in combatant.allies]
            everyone_but_combatant = list(self.combatants)
            everyone_but_combatant.remove(combatant)
            enemies = list(set(everyone_but_combatant) - set(combatant.allies))
            enemies_state = [enemy.get_enemy_state() for enemy in enemies]
            self.ui_manager.update_turn_for(combatant, self.get_current_combatant(), allies_state, enemies_state)


    def lookup_input(self, turn_input):
        caster_id = turn_input['caster_id']
        skill_id = turn_input['skill_id']
        target_id = turn_input['target_id']
        target = None
        caster = None
        for combatant in self.combatants:
            if combatant.id == caster_id:
                caster = combatant

            if combatant.id == target_id:
                target = combatant

        selected_skill = None
        for skill in caster.active_skills:
            if skill.id == skill_id:
                selected_skill = skill

        return selected_skill, target



    def add_global_pre_listener(self, listener:Character):
        self.global_pre_conditional_listeners.append(listener)

    def add_global_post_listener(self, listener:Character):
        self.global_post_conditional_listeners.append(listener)