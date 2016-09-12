from collections import OrderedDict

class CombatLogger:
    def __init__(self):
        self.turn = None
        self.previous_turns = []
        self.turn_index = 0
        self.round_index = 0

    def set_round_index(self, round_index):
        self.round_index = round_index

    def log_start_turn(self):
        self.turn_index += 1
        self.turn = Turn(self.turn_index, self.round_index)

    def log_end_turn(self):
        self.previous_turns.append(self.turn)
        self.turn = None

    def log_pre_reaction_update(self, pre_reaction, status_updates):
        old_updates = self.turn.pre_reaction_updates.get(pre_reaction.to_string(), [])
        new_updates = old_updates + status_updates
        self.turn.pre_reaction_updates[pre_reaction.to_string()] = new_updates

    def log_payload_update(self, skill_cast, status_updates):
        self.turn.payload_updates_list.append(status_updates)
        payload_str = " ".join([status_update.log for status_update in status_updates])
        self.turn.cast = skill_cast
        #initialize post reactions for status updates from skill cast
        self.turn.post_reaction_updates[payload_str] = OrderedDict()
        self.turn.current_payload_update_str = payload_str

    def log_post_reaction_update(self, post_reaction, status_updates):
        dict_for_payload = self.turn.post_reaction_updates[self.turn.current_payload_update_str]
        old_updates =  dict_for_payload.get(post_reaction.to_string(), [])
        new_updates = old_updates + status_updates
        dict_for_payload[post_reaction.to_string()] = new_updates

class Turn():
    def __init__(self, index, round_index):
        self.index = index
        self.round_index = round_index
        self.pre_reaction_updates = OrderedDict() #keys: pre_reaction.to_string(), values:[StatusUpdate]
        self.cast = None #SkillCast
        self.payload_updates_list = [] #[[StatusUpdate]] list of lists because we need to associate with updates per target
        self.post_reaction_updates = dict() #keys: [StatusUpdate] to string, values:OrderedDict(keys: [post_reaction.tostring(), values:[StatusUpdate]
        self.current_payload_update_str = None

    def json(self):

        #if there are any pre_reactions
        cast_str = ""
        if self.cast:
            cast_str = self.cast.description()

        pre_reaction_lines = []
        if self.pre_reaction_updates:

            for pre_reaction_str, status_updates in self.pre_reaction_updates.items():
                update_str = " ".join(status_updates)
                pre_reaction_lines.append("{0}: {1}".format(pre_reaction_str, update_str))
        pre_reactions = "\n".join(pre_reaction_lines) #return this

        payloads_and_post_reactions = dict() #return this
        for payload_updates in self.payload_updates_list:
            payload_str = " ".join([status_update.log for status_update in payload_updates])
            dict_for_payload = self.post_reaction_updates[payload_str]
            post_reaction_lines = []
            if dict_for_payload:
                for post_reaction_str, status_updates in dict_for_payload.items():
                    update_str = " ".join(status_updates)
                    post_reaction_lines.append("{0}: {1}").format(post_reaction_str, update_str)
            post_reactions = "\n".join(post_reaction_lines)

            #this is all you need to worry about
            payloads_and_post_reactions[payload_str] = post_reactions

        #TODO: have a list of payload update strs so we can do it in order
        return {"index": self.index,
                "round_index": self.round_index,
                "pre_reactions":pre_reactions,
                "skill_cast":cast_str,
                "payloads_and_post_reactions": payloads_and_post_reactions}






