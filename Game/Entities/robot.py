from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.gameState import GameState

from pygame import Vector2
from pygame.key import ScancodeWrapper
from pygame import mixer
import pygame

from Game.Entities.actor import Actor


class BasicRobot(Actor):
    """The BasicRobot class represents a playable basic robot with a position, radius and direction."""

    number: int
    """The number identifier (1, 2, ...) of this robot"""

    def __init__(self, gameState: 'GameState', texturePath: str, position: Vector2, number: int):
        texture = pygame.image.load(texturePath)
        direction = 0
        currentSpeed = 0
        hp = 100
        maxSpeed = 2
        acceleration = 0.05
        brakeAcceleration = 0.1
        rotationalSpeed = 3
        bulletSpeed = 5
        shootCooldown = 500
        shootRange = 200
        super().__init__(gameState, texture, position, direction, currentSpeed, maxSpeed, acceleration,
                         brakeAcceleration, rotationalSpeed, hp, bulletSpeed, shootCooldown, shootRange)
        self.number = number

    def updateMovement(self, pressed: ScancodeWrapper):
        keys = {1: [pygame.K_w,  pygame.K_a,    pygame.K_s,    pygame.K_d,     pygame.K_SPACE],
                2: [pygame.K_UP, pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_RSHIFT]}

        if pressed[keys[self.number][3]]:  # Right
            self.rotateRight()
        if pressed[keys[self.number][1]]:  # Left
            self.rotateLeft()
        if pressed[keys[self.number][2]]:  # Down
            self.brake()
        if pressed[keys[self.number][0]]:  # Up
            self.accelerate()
        if pressed[keys[self.number][4]]:  # Shooting
            self.shoot()

    def move(self):
        super().move()
        for deadlyObstacle in self.gameState.deadlyObstacles:
            if self.getHitBox().colliderect(deadlyObstacle):
                self.hit(1)

        for otherRobot in self.gameState.robots:
            if otherRobot.number == self.number:
                continue
            if (not otherRobot.isAlive) and self.getHitBox().colliderect(otherRobot.getHitBox()):
                otherRobot.revive()

    def handleKeyPresses(self, pressed: ScancodeWrapper):
        self.updateMovement(pressed)

    def kill(self):
        """Kills the robot and checks for game over"""
        if self.isAlive:
            mixer.Sound('Assets/Sounds/explosion.wav').play()
        super().kill(False)
        self.gameState.checkGameOver()

    def revive(self):
        self.isAlive = True
        self.hp = 100
