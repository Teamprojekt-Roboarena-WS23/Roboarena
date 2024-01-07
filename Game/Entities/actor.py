from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.gameState import GameState

from pygame import Vector2, Surface
import pygame
from pygame import mixer

from Game.Entities.entity import Entity
from Game.Entities.bullet import Bullet


class Actor(Entity):
    """An actor is an entity that can actively move, shoot, etc: A robot or an enemy."""

    maxSpeed: float
    """Maximum possible velocity"""

    acceleration: float
    """How much the velocity increases when initiating movement"""

    brakeAcceleration: float
    """How much the velocity decreases when braking"""

    rotationalSpeed: float
    """How many degrees the robot can turn per frame"""

    hp: int
    """Current amount of health points"""

    maxHp: int
    """Maximum possible amount of health points"""

    bulletSpeed: float
    """Speed of the bullet"""

    shootCooldown: float
    """Time an Actor has to wait till the next bullet is created"""

    shootRange: int
    """Range the weapon of the Actor"""

    def __init__(self, gameState: 'GameState', texture: Surface, position: Vector2,
                 direction: Vector2, currentSpeed: float, maxSpeed: float, acceleration: float,
                 brakeAcceleration: float, rotationalSpeed: float, hp: int, bulletSpeed: float,
                 shootCooldown: float, shootRange: int):
        super().__init__(gameState, texture, position, direction, currentSpeed)
        self.maxSpeed = maxSpeed
        self.acceleration = acceleration
        self.brakeAcceleration = brakeAcceleration
        self.rotationalSpeed = rotationalSpeed
        self.hp = hp
        self.maxHp = hp
        self.bulletSpeed = bulletSpeed
        self.shootCooldown = shootCooldown
        self.shootRange = shootRange

        self.lastShotTime = 0  # Needed for tracking the cooldown

    def accelerate(self):
        self.currentSpeed = min(self.currentSpeed + self.acceleration, self.maxSpeed)

    def brake(self):
        self.currentSpeed = max(self.currentSpeed - self.brakeAcceleration, 0)

    def rotateRight(self):
        self.rotate(self.rotationalSpeed)

    def rotateLeft(self):
        self.rotate(-self.rotationalSpeed)

    def shoot(self):
        """Create and return a bullet entity or None based on the current state of the cooldown."""
        if self.isAlive and self.updateShootCooldown():
            bulletTexture = pygame.Surface((5, 5))
            bulletTexture.fill((255, 0, 0))  # Do we have some textures for the bullets?
            bulletPosition = self.position + (self.size / 2)  # Looks best like this
            bullet = Bullet(self.gameState, bulletTexture, bulletPosition,
                            self.direction, self.bulletSpeed, self.shootRange, self)
            self.gameState.entities.append(bullet)
            mixer.Sound('Assets/Sounds/laser_gun_standard.wav').play()
            return bullet
        return None

    def updateShootCooldown(self):
        """Update the shooting cooldown."""
        current_time = pygame.time.get_ticks()
        if (current_time - self.lastShotTime) > self.shootCooldown:
            self.lastShotTime = current_time
            return True
        return False

    def hit(self, damage):
        super().hit(damage)
        self.hp -= damage
        if self.hp <= 0:
            self.kill()

    def drawHealthBar(self, surface: Surface):
        """Draws the health bar for this actor"""
        if self.hp > 0:
            healthbar = pygame.Surface((self.hp / 2, 2))
            healthbar.fill((50, 205, 50))
            surface.blit(healthbar, self.position + Vector2(-8, -6))
