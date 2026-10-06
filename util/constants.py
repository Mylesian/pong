import pygame.font

# these are constants for various things i just put them all here so i can use them wherever
# you can import whichever class has the things you want theyre grouped by what they affect

class data_constants:
    STAGE_DATA_PATH = 'data/stages.txt'
    WAVES_DATA_PATH = 'data/waves.txt'

class screen_constants:
    SCREEN_COLOR = (100, 100, 100)
    FPS = 60
    GAME_FONT = pygame.font.SysFont("Times New Roman", 30)
    BLOCK_IMAGE_X_OFFSET = 5
    FONT_X_OFFSET = GAME_FONT.get_height() + BLOCK_IMAGE_X_OFFSET
    HEALTH_FONT_COLOR = (200, 0, 0)
    MONEY_FONT_COLOR = (255, 228, 0)
    MONEY_Y_OFFSET = GAME_FONT.get_height()
    COIN_IMAGE = pygame.transform.scale(pygame.image.load('assets/coin.png').convert_alpha(), (GAME_FONT.get_height(), GAME_FONT.get_height()))
    QUIT_BGCOLOR = (255, 255, 255)
    QUIT_TXTCOLOR = (0, 0, 0)

class player_constants:
    PLAYER_MAX_HP = 100
    START_MONEY = 100
    TOWER_RADIUS = 35
    BASE_TOWER_IMAGE = pygame.transform.scale(pygame.image.load('assets/base_tower.png').convert_alpha(),
                                              (2 * TOWER_RADIUS, 2 * TOWER_RADIUS))
    TOWER_VIEW_RADIUS = 100
    TOWER_VIEW_RADIUS_SQUARED = TOWER_VIEW_RADIUS ** 2
    NOT_PLACED = 0
    PLACED = 1

class projectile_constants:
    PROJECTILE_SPEED = 10
    PROJECTILE_RADIUS = 3
    PROJECTILE_IMAGE = pygame.transform.scale(pygame.image.load('assets/projectile.png').convert_alpha(),
                                              (2 * PROJECTILE_RADIUS, 2 * PROJECTILE_RADIUS))

class stage_constants:
    STAGE_DIMENSIONS = (1200, 760)
    STAGE_COLOR = (25, 25, 25)
    TRACK_COLOR = (0, 255, 0)
    TRACK_THICKNESS = 5
    SHOP_BGCOLOR = (50, 50, 50)
    SHOP_WIDTH = player_constants.TOWER_RADIUS * 2
    BASE_WAVE_MONEY_GAIN = 100
    WAVE_MONEY_INCREMENT = 50
    WAVE_BUTTON_WIDTH = 60
    WAVE_BUTTON_IMAGE = pygame.transform.scale(pygame.image.load('assets/next_wave_button.png').convert_alpha(),
                                               (WAVE_BUTTON_WIDTH, WAVE_BUTTON_WIDTH))

class enemy_constants:
    ENEMY_RADIUS = 20
    ENEMY_BASE_SPEED = 1
    ENEMY_IMAGE_1HP = pygame.transform.scale(pygame.image.load('assets/enemy_1hp.png').convert_alpha(),
                                             (2 * ENEMY_RADIUS, 2 * ENEMY_RADIUS))
    ENEMY_IMAGE_2HP = pygame.transform.scale(pygame.image.load('assets/enemy_2hp.png').convert_alpha(),
                                             (2 * ENEMY_RADIUS, 2 * ENEMY_RADIUS))