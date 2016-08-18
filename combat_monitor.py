from threading import Lock

#this needs to handle getting state from the thread too

class CombatMonitor:
    def __init__(self, combat_manager):
        self.turn_lock = Lock()
        self.combat_manager = combat_manager

    def signal_times_up(self, current_combatant_name:str) -> bool:
        with self.turn_lock:
            if self.combat_manager.get_current_combatant().name == current_combatant_name:
                self.combat_manager.turn_time_up()
                return True
            return False

    def send_input(self, turn_input, current_combatant_name:str) -> bool:
        with self.turn_lock:
            if self.combat_manager.get_current_combatant().name == current_combatant_name:
                self.combat_manager.resolve_turn(turn_input)
                return True
            return False
