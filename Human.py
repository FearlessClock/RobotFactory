from pygame.math import Vector2

from Creature import Creature
from Map import Map
from TaskList import TaskList, Task


class Human(Creature):
    def __init__(self, x, y, tileLoader, tileSize, target, task):
        Creature.__init__(self, x, y, tileLoader, tileSize, 3)
        self.image = tileLoader.getTileFromName("mapTiles", 6)
        self.positionToGoTo: Vector2 = target
        self.lifeTask: Task = task
        self.brain.pushState(self.walkingToState)
        self.alive = True

    # Walking to state

    def walkingToState(self, level: Map):
        self.currentState = "Walking"
        if self.positionToGoTo is not None:
            gridSpaceGoTo = Vector2(self.positionToGoTo.x / self.tileSize.x,
                                    self.positionToGoTo.y / self.tileSize.y)
            self.moveToNode(level, level.getTileAt(gridSpaceGoTo))

            distanceToTask = self.positionToGoTo.distance_to(self.pos)
            if distanceToTask < 5:
                self.positionToGoTo = None
                self.brain.pushState(self.listeningState)
        if self.lifeTask.taskFinished:
            self.brain.pushState(self.leaveState)

    # Listening state
    def listeningState(self, level):
        self.currentState = "Listening"
        if self.lifeTask.taskFinished:
            self.brain.popState()

    def leaveState(self, level):
        self.currentState = "Leaving"
        if self.positionToGoTo is None:
            self.positionToGoTo = Vector2(19*self.tileSize.x,5*self.tileSize.y)
        else:
            gridSpaceGoTo = Vector2(self.positionToGoTo.x / self.tileSize.x,
                                    self.positionToGoTo.y / self.tileSize.y)
            self.moveToNode(level, level.getTileAt(gridSpaceGoTo))
        distanceToTask = self.positionToGoTo.distance_to(self.pos)
        if distanceToTask < 5:
            self.alive = False

    def update(self, level: Map, dt: int):
        """Update the AI. Brain and needs"""
        self.brain.update(level)
