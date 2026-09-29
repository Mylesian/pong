import pygame
import level.stage as stage
from util.timer import Timer
from util.constants import (
    GAME_FONT,
    FONT_X_OFFSET,
    HEALTH_FONT_COLOR,
    MONEY_FONT_COLOR,
    MONEY_Y_OFFSET,
    BLOCK_IMAGE_X_OFFSET,
    STAGE_DATA_PATH,
    SCREEN_COLOR,
    FPS,
    PLAYER_MAX_HP
)

class Game:
    def __init__(this):
        with open(STAGE_DATA_PATH) as stage_info:
            info = stage_info.read().split('\n')
        this.current_stage = stage.Stage(info[0])
        
        this.current_hp = PLAYER_MAX_HP
        this.coin_image = pygame.transform.scale(pygame.image.load('assets/coin.png').convert_alpha(),
                                                 (GAME_FONT.get_height(), GAME_FONT.get_height()))
        
    def get_info_block(this) -> pygame.Surface:
        hp_block = GAME_FONT.render(f'{this.current_hp}', False, HEALTH_FONT_COLOR)
        money_block = GAME_FONT.render('0', False, MONEY_FONT_COLOR)
        
        return hp_block, money_block
    
    def lose(this):
        pass
    
    def run(this, screen: pygame.Surface):
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            dt = 1/FPS

            screen.fill(SCREEN_COLOR)
            
            if this.current_hp == 0:
                this.lose()
            
            screen.blit(this.current_stage.update(this, dt), (0,0))
            
            hp_block, money_block = this.get_info_block()
            screen.blit(hp_block, (FONT_X_OFFSET, 0))
            screen.blit(money_block, (FONT_X_OFFSET, MONEY_Y_OFFSET))
            
            screen.blit(this.coin_image, (BLOCK_IMAGE_X_OFFSET, MONEY_Y_OFFSET))
              
            pygame.display.flip()
            clock.tick(FPS)