import pygame
from util.constants import (
    screen_constants as sc
)

# button !! click it and it does whatever action you pass through it
class Button(pygame.Rect):
    def __init__(this, bounds: tuple[float], display: pygame.Surface, action):
        super().__init__(bounds[0], bounds[1], display.get_width(), display.get_height())
        this.display = display
        this.action = action
        
    def draw(this, screen: pygame.Surface):
        screen.blit(this.display, (this.x + this.w / 2 - this.display.get_width() / 2, this.y + this.h / 2 - this.display.get_height() / 2))
        
    def update(this, mouse_just_pressed: bool):
        if mouse_just_pressed and this.collidepoint(pygame.mouse.get_pos()):
            return this.action()