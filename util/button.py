import pygame
from util.constants import (
    screen_constants as sc
)

# button !! display param can be a string or an image
# if display is a string you also need to specify bgcolor and txtcolor
class Button(pygame.Rect):
    def __init__(this, bounds: tuple[float], display, action, bgcolor: tuple[int] = None, txtcolor: tuple[int] = None):
        super().__init__(bounds)
        this.display = display
        this.action = action
        this.bgcolor = bgcolor
        this.txtcolor = txtcolor
    
    def draw(this, screen: pygame.Surface):
        if type(this.display) == str:
            render = sc.GAME_FONT.render(this.display, False, this.txtcolor)
            pygame.draw.rect(screen, this.bgcolor, this)
        else: render = this.display
            
        screen.blit(render, (this.x + this.w / 2 - render.get_width() / 2, this.y + this.h / 2 - render.get_height() / 2))
        
    def update(this, mouse_pressed: bool):
        if mouse_pressed and this.collidepoint(pygame.mouse.get_pos()):
            this.action()