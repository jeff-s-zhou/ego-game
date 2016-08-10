


class Character:
    def __init__(self, name, socket_id, stats, active_skills_list, passive_skills_list):
        self.name = name
        self.socket_id = socket_id
        self.state = stats
        self.active_skills_list = active_skills_list
        self.passive_skills_list = passive_skills_list

    def casts(self, skill_class, target):
        # legal = check_legal_arguments(skill_name, arguments)
        # if legal, blah blah
        # skill = get_skill(skill_name, arguments))
        # skill.cast(self, arguments.target)

        #see if we can actually do this
        skill = skill_class(self)

        skill.activate(target)