from character import Character, Stats
import active_skills


#TODO: this is probably going to end up being a global between all the threads that needs a monitor
class IdentityManager:
    def __init__(self):
        self.sid_to_character_dict = dict()
        self.character_to_sid_dict = dict()

        character1_stats = Stats(300, 40, 3, 3, 0, 50)
        character1 = Character(1, "Larken", character1_stats)
        slash1 = active_skills.Slash(character1)
        heal1 = active_skills.Heal(character1)
        tbh1 = active_skills.ThornBindHostage(character1)
        character1.set_skills([slash1, heal1, tbh1], [])

        character2_stats = Stats(400, 40, 4, 3, 0, 50)
        character2 = Character(2, "Shamshir", character2_stats)
        heal2 = active_skills.Heal(character2)
        slash2 = active_skills.Slash(character2)
        protect2 = active_skills.Protect(character2)
        character2.set_skills([slash2, heal2, protect2], [])

        character3_stats = Stats(500, 40, 5, 3, 0, 50)
        character3 = Character(3, "Ilfantz", character3_stats)
        heal3 = active_skills.Heal(character3)
        slash3 = active_skills.Slash(character3)
        protect3 = active_skills.Protect(character3)
        character3.set_skills([slash3, heal3, protect3], [])

        allies2 = [character3]
        allies3 = [character2]
        allies1 = []

        character1.set_allies(allies1)
        character2.set_allies(allies2)
        character3.set_allies(allies3)

        self.combatants = [character1, character2, character3]
        self.temp_combatants = list(self.combatants)


    def get_sid(self, combatant):
        return self.character_to_sid_dict[combatant]


    #TODO: hook this up with actual server integration
    def get_combatants(self):
        return self.combatants


    def register_sid_with_account(self, sid):
        character = self.temp_combatants.pop()
        self.sid_to_character_dict[sid] = character
        self.character_to_sid_dict[character] = sid
        return character

    def get_account(self, sid):
        pass

    def get_character(self, sid):
            return self.sid_to_character_dict[sid]

    def all_combatants_present(self):
        return not self.temp_combatants

