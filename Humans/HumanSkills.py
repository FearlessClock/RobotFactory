from random import random

from Collection.eSkills import eSkills


class HumanSkills:
    def __init__(self):
        self.stubbornness = random()*10

    def getSkillFromEnum(self, skillEnum):
        if skillEnum == eSkills.STUBBORNNESS:
            return self.stubbornness