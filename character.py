import combat
import conditionals
from combat import SkillCast

class Stats():
    def __init__(self, max_hp:int, max_mp:int, initiative:int, damage:int, defense:int):
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.initiative = initiative
        self.damage = damage
        self.defense = defense

class State():
    def __init__(self, hp, mp, status_effects):
        self.hp = hp
        self.mp = hp
        self.status_effects = status_effects

    def copy(self):
        return State(self.hp, self.mp, self.status_effects)

class StateUpdate():
    def __init__(self, old_state, new_state, log):
        self.old_state = old_state
        self.new_state = new_state
        self.log = log

class Character:
    def __init__(self, id:int, name:str, stats:Stats):
        self.id = id
        self.name = name
        self.stats = stats
        self.state = State(self.stats.max_hp, self.stats.max_mp, [])
        self.combat_logger = None

    def set_skills(self, active_skills, passive_skills):
        self.active_skills = active_skills
        self.passive_skills = passive_skills

    def set_allies(self, allies):
        self.allies = allies

    def casts(self, skill, target):
        # legal = check_legal_arguments(skill_id, arguments)
        # if legal, blah blah
        # skill.cast(self, arguments.target)

        return skill.cast(target)


    def tweak_cast(self, cast, combat_logger):
        pre_reactions = []
        modified_cast = cast
        for listener in self.get_pre_listeners():
            pre_reaction = listener.respond_to(cast)
            pre_reactions.append(pre_reaction)

        return modified_cast, pre_reactions

    def add_status(self, status):
        old_state = self.state
        new_state = old_state.copy()
        new_state.status_effects.append(status)
        log = "{0} is inflicted with {1}.".format(self.name, status.applied_to_string())
        return self.state_change_process(old_state, new_state, log)

    #TODO
    def remove_status(self, status):
        pass
        #self.state.status_effects.remove(status)

    def take_damage(self, damage):
        old_state = self.state
        new_state = old_state.copy()
        new_state.hp = new_state.hp - (damage - self.stats.defense)
        log = "{0} takes {1} damage.".format(self.name, damage)
        return self.state_change_process(old_state, new_state, log)

    def reduce_mp(self, mp):
        old_state = self.state
        new_state = old_state.copy()
        new_state.mp = new_state.mp - mp
        log = ""
        return self.state_change_process(old_state, new_state, log)

    def state_change_process(self, old_state, new_state, log):
        update = StateUpdate(old_state, new_state, log)
        reactions = self.signal_internal_conditions(update)
        self.state = new_state

        return reactions, update

    #TODO
    def signal_internal_conditions(self, state_update):
        pass


    def get_pre_listeners(self):
        return_list = []
        for status in self.statuses:
            #I miss pattern matching
            if status.__class__ == conditionals.PreConditional:
                if status.is_castable():
                    return_list.append(status)
        return return_list


    def get_post_listeners(self):
        return_list = []
        for status in self.statuses:
            #I miss pattern matching
            if status.__class__ == conditionals.PostConditional:
                if status.is_castable():
                    return_list.append(status)
        return return_list


    #ticker functions
    def my_turn_start(self):
        for status in self.statuses:
            status.turn_tick()
        self.statuses = [item for item in self.statuses if item.is_valid() == True]
        for active_skill in self.active_skills:
            active_skill.turn_tick()


    #state update functions
    def get_ally_state(self):
        status_states = [status.to_dict() for status in self.state.status_effects if status.is_visible()]
        return {'id': self.id, 'name': self.name, 'hp': self.state.hp, 'mp': self.state.mp, 'status': status_states}

    def get_enemy_state(self):
        status_states = [status.to_dict() for status in self.state.status_effects if status.is_visible()]
        injured = self.state.hp < self.stats.max_hp/4
        return {'id': self.id, 'name': self.name, 'injured': injured, 'status': status_states}

    def get_state(self):
        status_states = [status.to_dict() for status in self.state.status_effects if status.is_visible()]
        active_skill_states = [skill.to_dict() for skill in self.active_skills]
        return {'id': self.id, 'name': self.name, 'hp': self.state.hp, 'mp': self.state.mp, 'status': status_states, 'active_skills_store':active_skill_states}






