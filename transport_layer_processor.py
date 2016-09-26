

#helper static class to process objects into json dicts for front end
class TransportLayerProcessor:
    def process_skills(self, skills, characters):
        pass

    def process_character(self, character, relation):
        if relation == "self":
            return {'relation':'self', 'id': character.id,
                    'name': character.name, 'stats': character.stats.to_dict(relation)}

        if relation == "ally":
            return {'relation': 'ally', 'id': character.id,
                    'name': character.name, 'stats': character.stats.to_dict(relation)}

        if relation == "enemy":
            return {'relation': 'enemy', 'id': character.id,
                    'name': character.name, 'stats': character.stats.to_dict(relation)}



    #process update for one character's all combatants
    def process_character_updates(self, characters):
        pass


    def process_character_update(self, character, relation):
        if relation == "self":
            return {'relation': 'self', 'id': character.id,
                    'state': character.state.to_dict(relation, character.stats)}

        if relation == "ally":
            return {'relation': 'ally', 'id': character.id,
                    'state': character.state.to_dict(relation, character.stats)}

        if relation == "enemy":
            return {'relation': 'enemy', 'id': character.id, 'state': character.state.to_dict(relation, character.stats)}


    def process_skill_updates(self, skills, enemies, allies, me):
        return [skill.to_dict() for skill in skills]