from threading import Lock

#this needs to handle getting state from the thread too

class CombatMonitor:
    def __init__(self):
        self.turn_lock = Lock()
        self.turn_input = None

    def get_input(self):
        with self.turn_lock:
            temp = self.turn_input
            self.turn_input = None
            return temp


    def send_input(self, turn_input) -> bool:
        with self.turn_lock:
            self.turn_input = turn_input

