from typing import List


class TimedEventParams:
    def __init__(self, atWhatTime: int, callback):
        self.atWhatTime = atWhatTime
        self.callback = callback

class TimedEvents:
    """Make things happen after a certain amount of time"""
    def __init__(self):
        self.elapsedTime = 0
        self.eventsToCheck: List[TimedEventParams] = []

    def addTimedEvent(self, time, callback):
        """Add an event to the list in order"""
        timedEvent = TimedEventParams(time+self.elapsedTime, callback)
        if len(self.eventsToCheck) > 0:
            addOnce = False
            for i in range(len(self.eventsToCheck)):
                if self.eventsToCheck[i].atWhatTime > timedEvent.atWhatTime:
                    self.eventsToCheck.insert(i, timedEvent)
                    break
        else:
            self.eventsToCheck.append(timedEvent)

    def updateTimer(self, dt):
        """Move the timer forward by deltaTime"""
        self.elapsedTime += dt
        for event in self.eventsToCheck:
            if event.atWhatTime < self.elapsedTime:
                event.callback()
                self.eventsToCheck.remove(event)
            if event.atWhatTime > self.elapsedTime:
                break
