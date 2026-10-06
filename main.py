import ctypes
import pygame
from pygame._sdl2 import Window
import asyncio

# init this stuff here before importing the rest so pygame & screen are imported for images in util.constants
user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
pygame.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1] - 30), pygame.RESIZABLE)
Window.from_display_module().maximize()
pygame.display.set_caption('Pong')

import game as g

game = g.Game(screen.get_size())

asyncio.run(game.run(screen))