import pygame
import os

tileWidth = 32
tileHeight = 32
windowWidth = tileWidth*32
windowHeight = tileHeight*24
titleHeight = windowHeight / 10


playerTiles = []
for tile in os.listdir('Assets/Player'):
    playerTiles.append(pygame.image.load('Assets/Player/' + tile))

# Random chances for enemies, in percent. These are rather low because they occur every frame, i.e. 60 times per second.
enemyChooseNewTargetChance = 5
enemyShootChance = 10
