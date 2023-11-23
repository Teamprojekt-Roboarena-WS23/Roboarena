from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.gameState import GameState

import pygame
from pygame import Surface, Vector2
from pygame.key import ScancodeWrapper

from utils import clamp, degreesToUnitVector


class Entity:
    """Interface for all entities that can move on the screen"""

    isAlive: bool
    """Indicates if the entity is currently alive and active"""

    texture: Surface
    """The graphical texture of the entity"""

    position: Vector2
    """Current position of the entity on the map"""

    direction: float
    """Angle in degrees indicating the direction in which the entity is facing"""

    currentSpeed: float
    """Indicates by how much the entity moves per frame (velocity)"""

    size: Vector2
    """Size (width = x, height = y) of the entity"""

    def __init__(self, gameState: 'GameState', texture: Surface, position: Vector2, direction: float, currentSpeed: float):
        self.gameState = gameState
        self.isAlive = True
        self.texture = texture
        self.position = position
        self.direction = direction
        self.currentSpeed = currentSpeed
        self.size = Vector2(texture.get_size())

    def draw(self, surface: Surface):
        """Draws the entity to the screen."""
        rotatedImage = pygame.transform.rotate(self.texture, -self.direction)
        rotatedRect = rotatedImage.get_rect()
        rotatedRect.center = self.position + (self.size / 2)
        surface.blit(rotatedImage, rotatedRect)

    def move(self):
        """Moves the entity based on its current direction and speed"""
        movementVector = self.currentSpeed * degreesToUnitVector(self.direction)
        newPosition = self.position + movementVector
        newPosition.x = clamp(newPosition.x, 0, self.gameState.worldSize.x - self.size.x)
        newPosition.y = clamp(newPosition.y, 0, self.gameState.worldSize.y - self.size.y)
        self.position = newPosition

    def rotate(self, rotateBy: int):
        """Rotates the entity by rotateBy degrees"""
        self.direction = (self.direction + rotateBy) % 360

    def handleKeyPresses(self, pressed: ScancodeWrapper):
        """This method can be overridden by subclasses to handle keys that are pressed down"""