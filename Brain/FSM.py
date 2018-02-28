from Map import Map


class FSM:
    def __init__(self):
        self.currentState = []

    def pushState(self, state):
        self.currentState.append(state)

    def popState(self):
        return self.currentState.pop()

    def update(self, level: Map):
        self.currentState[len(self.currentState)-1](level)