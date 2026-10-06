import pygame
from level import (
    stage as stage,
    shop as shop
)
import asyncio
import util.button as button
from util.constants import (
    screen_constants as sc,
    data_constants as dat,
    player_constants as p
)

class Game:
    # window crashes ??? when i take out screen_dimensions param so i guess it stays
    def __init__(this, screen_dimensions):
        # initialize stages from data file
        with open(dat.STAGE_DATA_PATH) as stage_info:
            info = stage_info.read().split('\n')
            
        stages: list[stage.Stage] = []
            
        for line in info:
            stages.append(stage.Stage(line))
            
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
            mouse_down_this_frame = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    this.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not mouse_down:
                        mouse_just_down = True
                    else: mouse_just_down = False
                    
                    mouse_down = True
                    mouse_down_this_frame = True
            
            if not mouse_down_this_frame:
                mouse_down = False
                mouse_just_down = False
            
            # used for counting down timers and things
            dt = 1/sc.FPS

            screen.fill(sc.SCREEN_COLOR)
            
            screen.blit(this.current_stage.update(mouse_just_down, dt), (0,0))
            
            hp_block, money_block = this.current_stage.get_info_block()
            screen.blit(hp_block, (sc.FONT_X_OFFSET, 0))
            screen.blit(money_block, (sc.FONT_X_OFFSET, sc.MONEY_Y_OFFSET))
            
            screen.blit(sc.COIN_IMAGE, (sc.BLOCK_IMAGE_X_OFFSET, sc.MONEY_Y_OFFSET))
            
            this.shop.update(mouse_just_down)
            screen.blit(this.shop.draw(), (this.current_stage.get_width(), 0))
            
            # only one button for now but there will be more later
            for b in this.buttons:
                b.update(mouse_just_down)
                b.draw(screen)
              
            pygame.display.flip()
            clock.tick(sc.FPS)
            await asyncio.sleep(0)
        
        pygame.quit()