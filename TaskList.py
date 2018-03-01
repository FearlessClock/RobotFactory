from pygame.math import Vector2


class Task:
    def __init__(self, placeToGo: Vector2, callback, timeToEnd):
        self.placeToGo = placeToGo
        self.callback = callback
        self.timeToEnd = timeToEnd

class TaskList:
    def __init__(self):
        self.listOfTasks = []

    def enqueueTask(self, task: Task):
        self.listOfTasks.append(task)

    def dequeueTask(self) -> Task:
        if len(self.listOfTasks) > 0:
            return self.listOfTasks.pop(0)
        else:
            return None