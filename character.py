import combat
import status_effects
from combat import SkillCast
import copy


class Stats():
    def __init__(self, max_hp:int, max_mp:int, initiative:int, damage:int, defense:int, init_balance:int):
        self.max_hp = max_hp
        self.max_mp = max_mp
        self.init_balance = init_balance
        self.initiative = initiative
        self.damage = damage
        self.defense = defense


    def to_dict(self, relation):
        if relation == "self":
            return {"max_hp": self.max_hp, "max_mp": self.max_mp, "init_balance": self.init_balance}
        if relation == "ally":
            return {"max_hp": self.max_hp, "max_mp": self.max_mp, "init_balance": self.init_balance}
        if relation == "enemy":
            return {}


class State():
    def __init__(self, hp, mp, balance, status_effects, conditionals, order=0):
        self.hp = hp
        self.mp = mp
        self.balance = balance
        self.status_effects = status_effects
        self.conditionals = conditionals
        self.order = order

    def copy(self):
        return copy.deepcopy(self)

        #return State(self.hp, self.mp, self.balance, self.status_effects, self.order)

    def to_dict(self, relation, stats):
        status_states = [status.to_dict() for status in self.status_effects if status.is_visible()]
        if relation == "self":
            return {"order": self.order, "hp": self.hp, "mp": self.mp,
                    "balance": self.balance, "status_effects": status_states}
        if relation == "ally":
            return {"order": self.order, "hp": self.hp, "mp": self.mp,
                    "balance": self.balance, "status_effects": status_states}
        if relation == "enemy":
            hp_estimate = round((self.hp/stats.max_hp) * 10)
            balance_estimate = round((self.balance/stats.init_balance) * 10)
            return {"order": self.order, "hp_estimate": hp_estimate,
                    "balance_estimate": balance_estimate, "status_effects": status_states}


class StateUpdate():
    def __init__(self, old_state, new_state, log):
        self.old_state = old_state
        self.new_state = new_state
        self.log = log

class Character:
    def __init__(self, id:int, name:str, stats:Stats):
        self.id = id
        self.name = name
        self.stats = stats
        self.state = State(self.stats.max_hp, self.stats.max_mp, self.stats.init_balance, [], [])

    def set_skills(self, active_skills, passive_skills):
        self.active_skills = active_skills
        self.passive_skills = passive_skills

    def set_allies(self, allies):
        self.allies = allies

    def casts(self, skill, target):
        # legal = check_legal_arguments(skill_id, arguments)
        # if legal, blah blah
        # skill.cast(self, arguments.target)

        return skill.cast(target)


    def tweak_cast(self, cast):
        pre_reactions = []
        for listener in self.get_listeners(status_effects.ConditionalType.pre):
            pre_reaction = listener.tweak(cast)
            if pre_reaction:
                pre_reactions.append(pre_reaction)

        return pre_reactions


    def receive(self, payload):
        reactions = []
        status_updates = []
        if self.state.hp <= 0:
            log = "{0} is already downed. ".format(self.name)
            reaction, status_update = self.state_change_process(self.state, self.state, log)
            return [reaction], [status_update]

        for event in payload:
            reaction = None
            status_update = None
            if event.type == combat.EventType.damage:
                reaction, status_update = self.take_damage(event.value)
            elif event.type == combat.EventType.add_status:
                reaction, status_update = self.add_status(event.value)
            elif event.type == combat.EventType.reduce_mp:
                reaction, status_update = self.reduce_mp(event.value)
            elif event.type == combat.EventType.heal:
                reaction, status_update = self.heal(event.value)
            elif event.type == combat.EventType.add_conditional:
                reaction, status_update = self.add_conditional(event.value)

            if reaction:
                reactions.append(reaction)
            if status_update:
                status_updates.append(status_update)

        return reactions, status_updates

    def add_conditional(self, conditional):
        old_state = self.state
        new_state = old_state.copy()
        new_state.conditionals.append(conditional)
        log = "{0} is {1}. ".format(self.name, conditional.applied_to_string())
        return self.state_change_process(old_state, new_state, log)

    def add_status(self, status):
        old_state = self.state
        new_state = old_state.copy()
        new_state.status_effects.append(status)
        log = "{0} is {1}. ".format(self.name, status.applied_to_string())
        return self.state_change_process(old_state, new_state, log)

    #TODO
    def remove_status(self, status):
        pass
        #self.state.status_effects.remove(status)

    def take_damage(self, damage):
        old_state = self.state
        new_state = old_state.copy()
        new_state.hp = new_state.hp - (damage - self.stats.defense)
        log = "{0} takes {1} damage. ".format(self.name, damage)
        return self.state_change_process(old_state, new_state, log)

    def reduce_mp(self, mp):
        old_state = self.state
        new_state = old_state.copy()
        new_state.mp = new_state.mp - mp
        log = ""
        return self.state_change_process(old_state, new_state, log)

    def heal(self, hp):
        old_state = self.state
        new_state = old_state.copy()
        new_state.hp = new_state.hp + hp
        log = "{0} is healed for {1} health. ".format(self.name, hp)
        return self.state_change_process(old_state, new_state, log)

    def state_change_process(self, old_state, new_state, log):
        update = StateUpdate(old_state, new_state, log)
        reactions = self.signal_internal_conditions(update)
        self.state = new_state

        return reactions, update

    #TODO
    def signal_internal_conditions(self, state_update):
        pass


    def get_listeners(self, type):
        return_list = []
        for conditional in self.state.conditionals:
            #I miss pattern matching
            if type in conditional.types:
                    if conditional.is_castable():
                        return_list.append(conditional)
        return return_list


    def set_order(self, order:int):
        self.state.order = order


    #ticker functions
    def my_turn_start(self):
        for status in self.state.status_effects:
            status.turn_tick()
        self.state.status_effects = [item for item in self.state.status_effects if item.is_valid() == True]
        for active_skill in self.active_skills:
            active_skill.turn_tick()


    #json functions
    def get_static_state(self, relation):
        if relation == "self":
            return {'relation':'self', 'id': self.id, 'name': self.name, 'stats': self.stats.to_dict(relation)}

        if relation == "ally":
            return {'relation': 'ally', 'id': self.id, 'name': self.name, 'stats': self.stats.to_dict(relation)}

        if relation == "enemy":
            return {'relation': 'enemy', 'id': self.id, 'name': self.name, 'stats': self.stats.to_dict(relation)}

    #state update functions
    def get_state(self, relation):
        if relation == "self":
            return {'relation':'self', 'id': self.id, 'state':self.state.to_dict(relation, self.stats)}

        if relation == "ally":
            return {'relation': 'ally', 'id': self.id, 'state':self.state.to_dict(relation, self.stats)}

        if relation == "enemy":
            return {'relation': 'enemy', 'id': self.id, 'state':self.state.to_dict(relation, self.stats)}

    def get_skill_states(self):
        return [skill.to_dict() for skill in self.active_skills]

