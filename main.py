import pygame
import asyncio

SCREEN_DIMENSIONS = (1200, 760)
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.RESIZABLE)

import game as g

game = g.Game()

asyncio.run(game.run(screen))