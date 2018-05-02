from abc import ABC, abstractmethod
from pygame.math import Vector2

class AbstractTask(ABC):
    def __init__(self, placeToGo: Vector2, callback, taskName):
        self.placeToGo: Vector2 = placeToGo
        self.callback = callback

        self.taskFinishedFlag = False
        self.taskName = taskName

        # If the task was successfully completed
        self.success = None

    def taskFinished(self):
        self.taskFinishedFlag = True
        if self.callback is not None:
            self.callback()

    @abstractmethod
    def checkTaskState(self):
        pass


class Task(AbstractTask):

    def __init__(self, placeToGo: Vector2, callback, amountOfWorkToFinishTask, successRate, skillRequired,
                 taskName=None):
        AbstractTask.__init__(self, placeToGo, callback, taskName)
        """
        Init the Task to accomplish
        :param placeToGo: World Space vector
        :param callback: Function to call when the task is finished
        :param amountOfWorkToFinishTask: Arbitrary work value
        :param successRate: How much skill is needed to successfully complete the task
        :param skillRequired: What skills are required to complete this task successfully
        """
        self.amountOfWorkToFinishTask = amountOfWorkToFinishTask
        self.successRate = successRate
        self.skillRequired = skillRequired
        self.workerSkill = -1
        self.workProgress = 0

    def workOnTask(self, amount, skills):
        """Work on the task till it is finished, then call the callback"""
        self.workProgress += amount
        if self.workProgress > self.amountOfWorkToFinishTask:
            print(self.taskFinishedFlag)
            skillLevel = skills.getSkillFromEnum(self.skillRequired)
            self.workerSkill = skillLevel
            if self.successRate < skillLevel:
                self.success = True
            else:
                self.success = False

            self.taskFinishedFlag = True
            self.callback()


    def checkTaskState(self):
        return self.taskFinishedFlag


class WaitTask(AbstractTask):
    def __init__(self, placeToGo: Vector2, callback, taskName, waitTask, skillRequired):
        AbstractTask.__init__(self, placeToGo, callback, taskName)
        self.waitTask = waitTask
        self.skillRequired = skillRequired

    def checkTaskState(self):
        waitFunctionState = self.waitTask.checkTaskState()
        if waitFunctionState:
            self.taskFinished()
            self.success = self.waitTask.success;
            return True
        return False


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
