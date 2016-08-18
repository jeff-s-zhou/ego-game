from character import Character, Stats
import active_skills

class RoomManager:
    def __init__(self):
        self.sid_to_character_dict = dict()
        self.character_to_sid_dict = dict()

        character1_stats = Stats(300, 40, 10, 3)
        character1 = Character("1", "Larken", character1_stats)
        slash1 = active_skills.Slash(character1)
        character1.set_skills([slash1], [])

        character2_stats = Stats(400, 40, 10, 3)
        character2 = Character("2", "Shamshir", character2_stats)
        slash2 = active_skills.Slash(character2)
        character2.set_skills([slash2], [])

        character3_stats = Stats(500, 40, 10, 3)
        character3 = Character("3", "Cakeblade", character3_stats)
        slash3 = active_skills.Slash(character3)
        character3.set_skills([slash3], [])
        self.combatants = [character1, character2, character3]


    def get_sid(self, combatant):
        return self.character_to_sid_dict[combatant]


    #TODO: hook this up with actual server integration
    def get_combatants(self):
        return self.combatants


    def get_character(self, sid):
        if sid in self.sid_to_character_dict:
            return self.sid_to_character_dict[sid]
        else:
            character = self.combatants.pop()
            self.sid_to_character_dict[sid] = character
            self.character_to_sid_dict[character] = sid
            return character


    def all_combatants_present(self):
        return not self.combatants

