""" Class representing the actions a user can perform on a square.
    A user action is anything that the creature won't do by it self
    like cleaning up a mess or making more food"""
class UserAction:
    def __init__(self, name, actionCallback):
        self.name = name
        self.actionCallback = actionCallback

    def getName(self):
        return self.name

    def getCallback(self):
        return self.actionCallback

    def __str__(self):
        return str(self.name)