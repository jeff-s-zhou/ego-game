import json
from collections import defaultdict
from typing import List

import constants
from character import Character
from combat import SkillCast
import ui_manager as ui
import input_listener as input
from combat_logger import CombatLogger
import event_interface
from shared import identity_manager


class CombatEvent(event_interface.EventInterface):
    def __init__(self, characters, event_type=None):
        super().__init__(characters, event_type)
        '''self.name = event_type.name
        self.initial_text = event_type.text
        self.next_event = event_type.next_event
        self.enemies = event_type.enemies'''

        self.turn_input = None

        self.characters = characters
        self.state = event_interface.State.start
        self.tick_type = event_interface.TickType.real_time
        self.combat_logger = CombatLogger()
        #duplicate so we don't mess with them I think?
        self.combatants = characters

        # TODO: make sure it's sorting the right way, resolve tiebreaks fairly
        self.combatants.sort(key=lambda combatant: combatant.stats.initiative)

        self.combatants.reverse() #now it's high initiative first
        [combatant.set_order(i) for i, combatant in enumerate(self.combatants)] #1 is highest initiative

        self.current_combatant_index = 0
        self.round_index = 1
        self.global_pre_conditional_listeners = []
        self.global_post_conditional_listeners = []
        # TODO: apply passives


    def get_current_combatant(self):
        return self.combatants[self.current_combatant_index]

    def next_turn(self):
        if self.current_combatant_index + 1 == len(self.combatants):
            self.current_combatant_index = 0
            self.round_index += 1
            self.combat_logger.set_round_index(self.round_index)
        else:
            self.current_combatant_index += 1

    def initialize(self):
        updates = []

        for character in self.characters:
            my_static_state = character.get_static_state("self")
            ally_static_states = [ally.get_static_state("ally") for ally in character.allies] + [my_static_state]
            everyone_but_character = list(self.combatants)
            everyone_but_character.remove(character)
            enemies = list(set(everyone_but_character) - set(character.allies))
            enemy_static_states = [enemy.get_static_state("enemy") for enemy in enemies]

            initializers = {'allies': ally_static_states, 'enemies':enemy_static_states}
            payload = {'type': ui.EventType.combat_event.value, 'initializers': initializers}
            initialize_combat = ui.UIUpdate(ui.UIEvent.set_event, payload, character)
            updates.append(initialize_combat)

        return updates

    def handle_input(self, client_input):
        if(client_input['type'] == 'turn input'):
            self.turn_input = client_input['value']
            return None

    #TODO: deal with invalid actors
    def update(self):
        if self.state == event_interface.State.start:
            self.combat_logger.set_round_index(self.round_index)
            self.combat_logger.log_start_turn()
            caster = self.get_current_combatant()
            caster.my_turn_start()
            self.state = event_interface.State.running
            return self.initial_combat_update()


        if self.state == event_interface.State.running:
            print(self.turn_input)
            if self.turn_input:
                skill, target = self.lookup_input(self.turn_input)
                skill_cast = self.get_current_combatant().casts(skill, target)
                self.resolve_cast(skill_cast)

            turn_log = self.combat_logger.turn.json()
            self.combat_logger.log_end_turn()
            self.next_turn()

            self.combat_logger.log_start_turn()
            caster = self.get_current_combatant()
            caster.my_turn_start()

            self.turn_input = None
            return self.combat_update(turn_log)

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
            for post_reaction in post_reactions:
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
                        self.combat_logger.log_post_reaction_update(global_reaction, status_updates)


    def initial_combat_update(self):
        updates = []
        for combatant in self.combatants:
            my_state = combatant.get_state("self")
            ally_states = [ally.get_state("ally") for ally in combatant.allies] + [my_state]
            everyone_but_combatant = list(self.combatants)
            everyone_but_combatant.remove(combatant)
            enemies = list(set(everyone_but_combatant) - set(combatant.allies))
            enemy_states = [enemy.get_state("enemy") for enemy in enemies]
            my_skill_states = combatant.get_skill_states()

            #TODO: this REALLY doesn't belong here
            for my_skill_state in my_skill_states:
                if my_skill_state['valid_targets'][0] == constants.Targets.single_ally.value:
                    my_skill_state['target_ids'] = [ally.id for ally in combatant.allies]
                elif my_skill_state['valid_targets'][0] == constants.Targets.single_enemy.value:
                    my_skill_state['target_ids'] = [enemy.id for enemy in enemies]

            a_update = ui.UIUpdate(ui.UICombatEvent.my_ally_states, ally_states, combatant)
            e_update = ui.UIUpdate(ui.UICombatEvent.my_enemy_states, enemy_states, combatant)
            s_update = ui.UIUpdate(ui.UICombatEvent.my_skill_states, my_skill_states, combatant)
            updates.append(a_update)
            updates.append(e_update)
            updates.append(s_update)

        turn_update = ui.UIUpdate(ui.UICombatEvent.current_turn, self.get_current_combatant().id)
        updates.append(turn_update)
        return updates

    #TODO: personalize logs
    def combat_update(self, turn_log):
        updates = self.initial_combat_update()
        log_update = ui.UIUpdate(ui.UICombatEvent.turn_log, turn_log)
        updates.append(log_update)
        return updates


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
