

class CombatLogger:
    def __init__(self):
        pass

    def current_turn_to_string(self):
        pass

    def combat_to_string(self):
        pass

    def log_start_round(self):
        pass

    def log_end_round(self):
        pass

    def log_start_turn(self):
        pass

    def log_end_turn(self):
        pass

    def log_pre_reaction_update(self, pre_reaction, status_updates):
        logs = [status_update.log for status_update in status_updates]
        logs_str = ". ".join(logs)
        self.current_pre_reactions[pre_reaction.to_string()].append(logs_str)

    def log_payload_update(self, skill_cast, status_updates):
        logs = [status_update.log for status_update in status_updates]
        logs_str = ". ".join(logs)
        self.current_skill_cast_str = skill_cast.to_string()
        self.current_payload_update_str = logs_str

    def log_post_reaction_update(self, post_reaction, status_updates):
        logs = [status_update.log for status_update in status_updates]
        logs_str = ". ".join(logs)
        current_post_reactions = self.current_payloads[self.current_payload_update_str]
        current_post_reactions[post_reaction.to_string()].append(logs_str)


