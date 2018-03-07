class Needs:
    """Class used to hold the needs of a clergy Robot"""

    def __init__(self):
        self.hunger = 100
        self.thirst = 100
        self.tired = 100
        self.boredom = 0

    def stepNeeds(self):
        self.hunger -= 1
        self.tired -= 1

    def isTired(self) -> bool:
        if self.tired < 40:
            return True
        else:
            return False

    def isHungry(self) -> bool:
        if self.hunger < 30:
            return True
        else:
            return False

    def eat(self, amount):
        self.hunger += amount

    def sleep(self, amount):
        self.tired += amount
