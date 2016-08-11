


class Character:
    def __init__(self, name, socket_id, stats, active_skills_list, passive_skills_list):
        self.name = name
        self.socket_id = socket_id
        self.state = stats
        self.active_skills_list = active_skills_list
        self.passive_skills_list = passive_skills_list

    def casts(self, skill_class, target_name, other_names):
        # legal = check_legal_arguments(skill_name, arguments)
        # if legal, blah blah
        # skill = self.get_skill(skill_name, arguments))
        # skill.cast(self, arguments.target)

        #see if we can actually do this
        skill = skill_class(self)
        events = skill.cast(target_name, other_names)
        for event in events:
            notify_conditionals(self.state, event)
            notify_global_conditionals(self.state, event)


    def receive(self, event):
        notify_conditionals(self.state, event)
        notify_global_conditionals(self.state, event)

        if (ok):
            event.do()

        else:
            'dont do it'

        notify_conditionals(self.state, event)
        notify_global_conditionals(self.state, event)

