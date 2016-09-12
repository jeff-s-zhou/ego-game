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

        self.combatants.reverse() #now it's high initiative first
        [combatant.set_order(i) for i, combatant in enumerate(self.combatants)] #1 is highest initiative

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
            self.combat_logger.set_round_index(self.round_index)
        else:
            self.current_combatant_index += 1

    # TODO: remove invalids actors
    def update(self):
        #initialize the round, before the first handle input
        if self.round_index == 0 and self.current_combatant_index == 0:
            self.round_index = 1
            self.combat_logger.set_round_index(self.round_index)
            self.ui_manager.combat_start()

        #this will be called after handle input
        else:
            turn_log = self.combat_logger.turn.json()
            self.call_update_log(turn_log)
            self.combat_logger.log_end_turn()
            self.next_turn()


        self.combat_logger.log_start_turn()
        caster = self.get_current_combatant()
        caster.my_turn_start()
        self.call_ui_update()


    def handle_input(self):
        turn_input = self.combat_monitor.get_input()
        if turn_input:
            skill, target = self.lookup_input(turn_input)
            skill_cast = self.get_current_combatant().casts(skill, target)
            self.resolve_cast(skill_cast)




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
                    null_reaction, status_updates = combatant.receive(pre_reaction.payloads[combatant.id])
                    self.combat_logger.log_pre_reaction_update(pre_reaction, status_updates)


    def do(self, skill_cast):
        for target in skill_cast.targets:

            # cast the skill, and give combatant an opportunity to react to state changes
            post_reactions, status_updates = target.receive(skill_cast.payloads[target.id])
            self.combat_logger.log_payload_update(skill_cast, status_updates)
            '''for post_reaction in post_reactions:
                for combatant in post_reaction.targets:
                    null_reaction, status_updates = combatant.receive(post_reaction.payloads[combatant.id])
                    self.combat_logger.log_post_reaction_update(post_reaction, status_updates)

            # give other interested combatants an opportunity to react to a combatant's state change
            for post_listener in self.global_post_conditional_listeners:
                # TODO: add the original skill cast to the sniff for things like lifesteal
                global_reactions = post_listener.sniff(status_updates)
                for global_reaction in global_reactions:
                    for combatant in global_reaction.targets:
                        null_reaction, status_updates = combatant.receive(global_reaction.payloads[combatant.id])
                        self.combat_logger.log_post_reaction_update(global_reaction, status_updates)'''


    def call_ui_update(self):
        for combatant in self.combatants:
            ally_states = [ally.get_state("ally") for ally in combatant.allies]
            everyone_but_combatant = list(self.combatants)
            everyone_but_combatant.remove(combatant)
            enemies = list(set(everyone_but_combatant) - set(combatant.allies))
            enemy_states = [enemy.get_state("enemy") for enemy in enemies]
            my_state = combatant.get_state("self")
            combatant_states = ally_states + enemy_states + [my_state]
            my_skill_states = combatant.get_skill_states()
            self.ui_manager.update_turn_for(combatant, combatant_states, my_skill_states, self.get_current_combatant())

    def call_update_log(self, turn_log):
        self.ui_manager.update_log(turn_log)


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

    def get_combatants_for_character(self, character):
        ally_static_states = [ally.get_static_state("ally") for ally in character.allies]
        everyone_but_character = list(self.combatants)
        everyone_but_character.remove(character)
        enemies = list(set(everyone_but_character) - set(character.allies))
        enemy_static_states = [enemy.get_static_state("enemy") for enemy in enemies]
        my_static_state = character.get_static_state("self")
        combatant_static_states = ally_static_states + enemy_static_states + [my_static_state]
        self.ui_manager.create_combatants_for(character, combatant_static_states)