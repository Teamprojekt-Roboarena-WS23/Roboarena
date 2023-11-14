from pygame import Vector2
from constants import windowWidth, windowHeight
from Game.arena import Arena
from Game.robot import BasicRobot


class GameState():
    def __init__(self, level: str) -> None:
        self.level = level
        self.worldSize = Vector2(windowWidth, windowHeight)
        self.tileSize = Vector2(32, 32)
        self.movementWidth = 3
        self.arena = Arena(self, level)

        self.robots = [BasicRobot(self,
                                  windowWidth / 4, windowHeight / 4,
                                  "Assets/player/anotherRed.png"),
                       BasicRobot(self,
                                  3 * windowWidth / 4, windowHeight / 4,
                                  "Assets/player/blue.png"),
                       BasicRobot(self,
                                  windowWidth / 4, 3 * windowHeight / 4,
                                  "Assets/player/deepblue.png"),
                       BasicRobot(self,
                                  3 * windowWidth / 4, 3 * windowHeight / 4,
                                  "Assets/player/gray.png")]
        self.activeRobot = 0

    def worldWidth(self):
        return self.worldSize.x

    def worldHeight(self):
        return self.worldSize.y

    def getMovementWidth(self):
        return self.movementWidth

    def getActiveRobot(self):
        return self.robots[self.activeRobot]

    def update(self, movementVector: Vector2, direction: int):
        self.robots[self.activeRobot].move(movementVector, self.worldWidth(), self.worldHeight())
        self.robots[self.activeRobot].rotate(direction)

    def draw(self, window):
        window.fill((0, 0, 0))
        self.arena.draw(window)
        for i in range(len(self.robots)):
            robot = self.robots[i]
            selected = i == self.activeRobot
            robot.draw(window, selected)

    def selectRobot(self, robotNo: int):
        self.activeRobot = robotNo
