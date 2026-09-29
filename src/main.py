import pygame

SCREEN_DIMENSIONS = (1200, 760)
pygame.init()
screen = pygame.display.set_mode(SCREEN_DIMENSIONS, pygame.RESIZABLE)

import game as g

game = g.Game()

game.run(screen)
pygame.quit()