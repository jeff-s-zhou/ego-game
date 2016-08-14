
class Debuff:
    def __init__(self):
        pass

    def remove(self):
        pass

    def tick(self):
        pass

    def untick(self):
        pass

    def undo(self):
        pass

class Poisoned(Debuff):
    def __init__(self):
        super().__init__()

    def remove(self):
        pass

    def tick(self):
        pass

    def untick(self):
        pass

    def undo(self):
        pass

    def isVisible(self):
        return True
