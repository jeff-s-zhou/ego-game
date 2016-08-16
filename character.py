

import conditionals
from combat import SkillCast

#TODO: probably need to just change all this to a serialize
class State():
    def __init__(self, character:Character):
        self.hp = character.hp
        self.mana = character.mana
        self.status_states = [status.get_state() for status in character.statuses]
        self.active_skill_states = [skill.get_state() for skill in character.active_skills]

class Character:
    def __init__(self, id, name, stats, active_skills, passive_skills):
        self.id = id
        self.name = name
        self.stats = stats
        self.hp = stats.max_hp
        self.mana = stats.max_mana
        self.statuses = None
        self.active_skills = active_skills
        self.passive_skills = passive_skills
        self.event_updates = []

    def casts(self, skill, target):
        # legal = check_legal_arguments(skill_name, arguments)
        # if legal, blah blah
        # skill = self.get_skill(skill_name, arguments))
        # skill.cast(self, arguments.target)

        return skill.cast(target)

    def get_state(self):
        return State(self)

    def get_pre_listeners(self):
        return_list = []
        for status in self.status:
            #I miss pattern matching
            if status.__class__ == conditionals.PreConditional:
                if status.is_castable():
                    return_list.append(status)
        return return_list

    def get_post_listeners(self):
        return_list = []
        for status in self.status:
            #I miss pattern matching
            if status.__class__ == conditionals.PostConditional:
                if status.is_castable():
                    return_list.append(status)
        return return_list

    def receive_cast(self, skill_cast:SkillCast):
        skill_cast.do()
        self.log(skill_cast)

    def add_status(self, status):
        self.statuses.append(status)

    #TODO
    def log(self, skill_cast):
        pass

    def remove_status(self, status):
        self.statuses.remove(status)

    #ticker functions
    def my_turn_start(self):
        for status in self.statuses:
            status.turn_tick()
        self.statuses = [item for item in self.statuses if item.is_valid() == True]
        for active_skill in self.active_skills:
            active_skill.turn_tick()

