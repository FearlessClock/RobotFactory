from random import random

from Collection.eSkills import eSkills


class ClergyRobotSkills:
    def __init__(self):
        self.convincing = random()*10

    def getSkillFromEnum(self, skillEnum):
        if skillEnum == eSkills.CONVINCING:
            return self.convincing