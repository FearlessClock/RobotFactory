from Map import Map


class MapHolder:
    """Class holding all the loaded maps"""

    def __init__(self, filenames, tileSize, tileLoader):
        self.mapNames = filenames
        self.maps = []
        self.loadedMap = None
        mapValues = []
        idValues = []
        self.currentMap = 1
        self.tileSize = tileSize
        for i in range(len(self.mapNames)):
            map = Map(self.mapNames[i], self.tileSize, tileLoader)
            mapValues.append(map)
            idValues.append(map.id)
        self.maps = dict(zip(idValues, mapValues))
        self.changeToMap(self.currentMap)

    def getCurrentMap(self):
        return self.loadedMap

    def changeToMap(self, Id):
        self.currentMap = int(Id)
        self.loadedMap = self.maps[self.currentMap]

    def getMapById(self, _id):
        for key, mapTested in self.maps.items():
            if mapTested.id == _id:
                return mapTested
        return None

    def drawMap(self, _id):
        self.maps.get(_id)
