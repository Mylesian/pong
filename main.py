import pygame
import asyncio

# init this stuff here before importing the rest so pygame & screen are imported for images in util.constants
screen_size = (1300, 760)
pygame.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1]), pygame.SCALED)
pygame.display.set_caption('Pong')

import game as g

game = g.Game(screen.get_size())

asyncio.run(game.run(screen))
