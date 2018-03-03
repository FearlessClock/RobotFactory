from pygame.math import Vector2


class Task:
    def __init__(self, placeToGo: Vector2, callback, amountOfWorkToFinishTask, taskName=None):
        """
        Init the Task to accomplish
        :param placeToGo: World Space vector
        :param callback: Function to call when the task is finished
        :param amountOfWorkToFinishTask: arbitrary work value
        """
        self.placeToGo: Vector2 = placeToGo
        self.callback = callback
        self.amountOfWorkToFinishTask = amountOfWorkToFinishTask
        self.workProgress = 0
        self.taskFinished = False
        self.taskName = taskName

    def workOnTask(self, amount):
        """Work on the task till it is finished, then call the callback"""
        self.workProgress += amount
        if self.workProgress > self.amountOfWorkToFinishTask:
            self.taskFinished = True
            self.callback()


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