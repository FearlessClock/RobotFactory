class Needs:
    """Class used to hold the needs of a clergy Robot"""

    def __init__(self):
        self.hunger = 50
        self.thirst = 100
        self.sleep = 100
        self.boredom = 0

    def stepNeeds(self):
        self.hunger -= 1
        self.sleep -= 1
