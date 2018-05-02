from Map import Map


class FSM:
    def __init__(self):
        self.currentState = []

    def pushState(self, state):
        self.currentState.append(state)

    def popState(self):
        return self.currentState.pop()

    def update(self, level: Map):
        if len(self.currentState) > 0:
            self.currentState[len(self.currentState)-1](level)
        else:
            print("You need to add some states")
