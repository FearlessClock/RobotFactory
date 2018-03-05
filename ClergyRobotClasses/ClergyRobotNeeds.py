class Needs:
    """Class used to hold the needs of a clergy Robot"""

    def __init__(self):
        self.hunger = 50
        self.thirst = 50
        self.sleep = 100
        self.boredom = 0

    def stepNeeds(self):
        self.hunger -= 1
        self.sleep -= 1

    def isTired(self) -> bool:
        if self.sleep < 40:
            return True
        else:
            return False

    def isHungry(self) -> bool:
        if self.hunger < 30:
            return True
        else:
            return False
