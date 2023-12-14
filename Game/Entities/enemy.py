from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.gameState import GameState
import random

import pygame

from constants import enemyChooseNewTargetChance, enemyShootChance
from utils import isRightOf
from Game.Entities.actor import Actor


class Enemy(Actor):
    def __init__(self, gameState: 'GameState', texturePath: str, position: pygame.Vector2):
        texture = pygame.image.load(texturePath)
        direction = 0
        currentSpeed = 0
        hp = 50
        maxSpeed = 2
        acceleration = 0.05
        brakeAcceleration = 0.005
        rotationalSpeed = 1
        bulletSpeed = 3
        shootCooldown = 500
        shootRange = 200
        super().__init__(gameState, texture, position, direction, currentSpeed, maxSpeed, acceleration,
                         brakeAcceleration, rotationalSpeed, hp, bulletSpeed, shootCooldown, shootRange)
        self.target = None

    def move(self):
        super().move()
        if self.isAlive:
            self.chooseTarget()
            if not self.target:
                self.brake()
                return

            finalAngle = self.chooseDirection()
            if abs(self.direction - finalAngle) >= 2 * self.rotationalSpeed:
                self.brake()
                if isRightOf(self.direction, finalAngle):
                    self.rotateLeft()
                else:
                    self.rotateRight()
            elif (self.position - self.target.position).length() >= 20:
                self.accelerate()
            else:
                self.brake()

            if random.randint(0, 100) < enemyShootChance:
                self.shoot()

    def kill(self):
        super().kill(False)
        self.gameState.checkGameOver()

    def chooseTarget(self):
        if (not self.target) or (random.randint(0, 100) < enemyChooseNewTargetChance):
            targets = [x for x in self.gameState.robots if x.isAlive]
            targets.sort(key=lambda x: (x.position - self.position).length())
            if not targets:
                return
            self.target = targets[0]

    def chooseDirection(self):
        baseDirection = 0
        if self.target:
            baseDirection = pygame.Vector2.angle_to(pygame.Vector2(0, 0), self.target.position - self.position) % 360
        return baseDirection
