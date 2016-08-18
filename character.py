

import conditionals
from combat import SkillCast

class Stats():
    def __init__(self, max_hp:int, max_mp:int, initiative:int, damage:int):
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.initiative = initiative
        self.damage = damage

class Character:
    def __init__(self, id:str, name:str, stats:Stats):
        self.id = id
        self.name = name
        self.stats = stats
        self.hp = stats.max_hp
        self.mp = stats.max_mp
        self.statuses = []
        self.event_updates = []

    def set_skills(self, active_skills, passive_skills):
        self.active_skills = active_skills
        self.passive_skills = passive_skills

    def casts(self, skill, target):
        # legal = check_legal_arguments(skill_name, arguments)
        # if legal, blah blah
        # skill = self.get_skill(skill_name, arguments))
        # skill.cast(self, arguments.target)

        return skill.cast(target)

    def get_basic_state(self):
        status_states = [status.to_dict() for status in self.statuses if status.is_visible()]
        return {'hp': self.hp, 'mp': self.mp, 'status': status_states}

    def get_state(self):
        status_states = [status.to_dict() for status in self.statuses if status.is_visible()]
        active_skill_states = [skill.to_dict() for skill in self.active_skills]
        return {'hp': self.hp, 'mp': self.mp, 'status': status_states, 'active_skills':active_skill_states}


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




