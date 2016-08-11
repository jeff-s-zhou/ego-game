




#get the role of the current player #
def get_precombat_state(player_count):
    pass


class CombatCharacterManager:
    def execute(self):
        pass


#wraps one execution of a player's skill
class Command:
    def __init__(self, skill):
        #pointer to skill
        self.skill = skill

    def do(self):
        self.skill.do()

    def undo(self):
        self.skill.undo()

