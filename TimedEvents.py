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
        if len(self.eventsToCheck) > 0:
            addOnce = False
            intermittence = []
            for evt in self.eventsToCheck:
                if not addOnce and evt.atWhatTime > time:
                    intermittence.append(TimedEventParams(time, callback))
                intermittence.append(evt)
            if not addOnce:
                intermittence.append(TimedEventParams(time, callback))
            self.eventsToCheck = intermittence
        else:
            self.eventsToCheck.append(TimedEventParams(time, callback))

    def updateTimer(self, dt):
        """Move the timer forward by deltaTime"""
        self.elapsedTime += dt
        for event in self.eventsToCheck:
            if event.atWhatTime < self.elapsedTime:
                event.callback()
                self.eventsToCheck.remove(event)
            if event.atWhatTime > self.elapsedTime:
                break
