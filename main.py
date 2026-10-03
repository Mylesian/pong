import pygame
import asyncio

# init this stuff here before importing the rest so pygame & screen are imported for images in util.constants
SCREEN_DIMENSIONS = (1200, 760)
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

import game as g

game = g.Game(screen.get_size())

asyncio.run(game.run(screen))