from globals import Globals

class Character:
    def __init__(self, name, socket_id, stats, active_skills_list, passive_skills_list):
        self.name = name
        self.socket_id = socket_id
        self.state = stats
        self.active_skills_list = active_skills_list
        self.passive_skills_list = passive_skills_list
        self.event_updates = []

    def casts(self, skill, target_name, other_names):
        # legal = check_legal_arguments(skill_name, arguments)
        # if legal, blah blah
        # skill = self.get_skill(skill_name, arguments))
        # skill.cast(self, arguments.target)

        return skill

    def receive_cast(self, skill_cast):
        skill_cast.do(self)
        self.log(skill_cast)

    def add_status_effects(self, status_effect):
        pass

    def log(self, skill_cast):
        pass