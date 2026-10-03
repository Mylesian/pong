import pygame
import level.stage as stage
import asyncio
import util.button as button
from util.constants import (
    screen_constants as sc,
    data_constants as dat,
    player_constants as p
)

class Game:
    def __init__(this, screen_dimensions):
        # initialize stages from data file
        with open(dat.STAGE_DATA_PATH) as stage_info:
            info = stage_info.read().split('\n')
            
        stages: list[stage.Stage] = []
            
        for line in info:
            stages.append(stage.Stage(line))
            
        this.current_stage = stages[0]
        this.current_hp = p.PLAYER_MAX_HP
        
        # put this here so quit button works
        this.running = True
        
        this.buttons: list[button.Button] = []
        
        # quit button just breaks out of the loop and closes the window
        def quit():
            this.running = False
        this.buttons.append(button.Button((screen_dimensions[0] - 100, 0, 100, 75), 'QUIT', quit, sc.QUIT_BGCOLOR, sc.QUIT_TXTCOLOR))
        
    # get surfaces with player info to write to the screen
    def get_info_block(this) -> pygame.Surface:
        hp_block = sc.GAME_FONT.render(f'{this.current_hp}', False, sc.HEALTH_FONT_COLOR)
        money_block = sc.GAME_FONT.render('0', False, sc.MONEY_FONT_COLOR)
        
        return hp_block, money_block
    
    # does nothing yet, will run the loss sequence when someone makes it
    def lose(this):
        pass
    
    # game loop here because i like oop and it makes main file cleaner
    async def run(this, screen: pygame.Surface):
        clock = pygame.time.Clock()
        
        mouse_down = False
        while this.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    this.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                else: mouse_down = False
            
            # used for counting down timers and things
            dt = 1/sc.FPS

            screen.fill(sc.SCREEN_COLOR)
            
            if this.current_hp == 0:
                this.lose()
            
            screen.blit(this.current_stage.update(this, mouse_down, dt), (0,0))
            
            hp_block, money_block = this.get_info_block()
            screen.blit(hp_block, (sc.FONT_X_OFFSET, 0))
            screen.blit(money_block, (sc.FONT_X_OFFSET, sc.MONEY_Y_OFFSET))
            
            screen.blit(sc.COIN_IMAGE, (sc.BLOCK_IMAGE_X_OFFSET, sc.MONEY_Y_OFFSET))
            
            # only one button for now but there will be more later
            # probably making the tower buy options into these buttons with the pictures of the towers on them
            for b in this.buttons:
                b.update(mouse_down)
                b.draw(screen)
              
            pygame.display.flip()
            clock.tick(sc.FPS)
            await asyncio.sleep(0)
        
        pygame.quit()