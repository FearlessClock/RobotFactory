""" Class representing the actions a user can perform on a square.
    A user action is anything that the creature won't do by it self
    like cleaning up a mess or making more food"""
class UserAction:
    def __init__(self, name, actionTask):
        self.name = name
        self.actionTask = actionTask

    def getName(self):
        return self.name

    def getTask(self):
        return self.actionTask

    def __str__(self):
        return str(self.name)