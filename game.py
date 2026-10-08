import pygame
from level import (
    stage as stage,
    shop as shop
)
import asyncio
import util.button as button
from util.constants import (
    screen_constants as sc,
    data_constants as dat
)

class Game:
    # window crashes ??? when i take out screen_dimensions param so i guess it stays
    def __init__(this, screen_dimensions):
        # initialize stages from data file
        with open(dat.STAGE_DATA_PATH) as stage_info:
            info = stage_info.read().split('\n')
            
        stages: list[stage.Stage] = []
            
        for line in info:
            stages.append(stage.Stage(screen_dimensions, line))
            
        this.current_stage = stages[0]
        
        # put this here so quit button works
        this.running = True
        
        this.buttons: list[button.Button] = []
        
        this.shop = shop.Shop(this.current_stage)
    
    # game loop here because i like oop and it makes main file cleaner
    async def run(this, screen: pygame.Surface):
        clock = pygame.time.Clock()
        
        mouse_down = False
        mouse_just_down = False
        while this.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    this.running = False
                
            mouse_buttons = pygame.mouse.get_pressed()
            if mouse_buttons[0]:
                if mouse_down: mouse_just_down = False
                else: mouse_just_down = True
                
                mouse_down = True
            else:
                mouse_down = False
                mouse_just_down = False
            
            # used for counting down timers and things
            dt = 1/sc.FPS

            screen.fill(sc.SCREEN_COLOR)
            
            if not this.current_stage == None:
                screen.blit(this.current_stage.update(mouse_just_down, dt), (0,0))
                
                if not this.current_stage.end_screen:
                    this.shop.update(mouse_just_down)
                
                hp_block, money_block = this.current_stage.get_info_block()
                screen.blit(hp_block, (sc.FONT_X_OFFSET, 0))
                screen.blit(money_block, (sc.FONT_X_OFFSET, sc.MONEY_Y_OFFSET))
                
                screen.blit(sc.COIN_IMAGE, (sc.BLOCK_IMAGE_X_OFFSET, sc.MONEY_Y_OFFSET))
                
                screen.blit(this.shop.draw(), (this.current_stage.get_width(), 0))
                
                if this.current_stage.end_screen:
                    screen.fill(sc.END_SCREEN_BG_DIM, special_flags = pygame.BLEND_RGB_SUB)
                    
                    msg = sc.GAME_FONT.render(this.current_stage.end_message, False, sc.UI_FONT_COLOR)
                    screen.blit(msg, ((screen.get_width() - msg.get_width()) / 2, screen.get_height() / 2 - 100))
                    
                    this.current_stage.restart_button.draw(screen)
                    st = this.current_stage.restart_button.update(mouse_just_down)
                    if not st is None:
                        this.current_stage = st
            
            for b in this.buttons:
                b.update(mouse_just_down)
                b.draw(screen)
              
            pygame.display.flip()
            clock.tick(sc.FPS)
            await asyncio.sleep(0)
        
        pygame.quit()