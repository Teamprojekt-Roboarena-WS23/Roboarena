from pytmx import load_pygame


class Arena():
    def __init__(self, gameState, level: str) -> None:
        self.gameState = gameState
        self.horizontalTiles = int(self.gameState.worldSize.x / self.gameState.tileSize.x)
        self.verticalTiles = int(self.gameState.worldSize.y / self.gameState.tileSize.y)
        self.tmxdata = load_pygame(f"Assets/Maps/level{level}.tmx")

    def drawBelowEntities(self, surface):
        self.drawLayers(surface, ["Ground", "Deadly"])

    def drawAboveEntities(self, surface):
        self.drawLayers(surface, ["WallsLowerHalf", "WallsLeftQuarter", "WallsRightQuarter", "Obstacles", "Decoration"])

    def drawLayers(self, surface, layerNames):
        for layerName in layerNames:
            for layer in self.tmxdata.layers:
                if layer.name == layerName:
                    for x, y, gid, in layer:
                        tile = self.tmxdata.get_tile_image_by_gid(gid)
                        if tile is not None:
                            surface.blit(tile, (x * self.tmxdata.tilewidth,
                                                y * self.tmxdata.tileheight))
