

class Gear():
    def __init__(self, **gear):
        self.head = None
        self.body = None
        self.leg = None
        self.weapon = None
        self.__dict__.update(gear)