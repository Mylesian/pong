import pygame.font

STAGE_DATA_PATH = 'data/stages.txt'
WAVES_DATA_PATH = 'data/waves.txt'

SCREEN_COLOR = (100, 100, 100)
FPS = 60
GAME_FONT = pygame.font.SysFont("Times New Roman", 30)
BLOCK_IMAGE_X_OFFSET = 5
FONT_X_OFFSET = GAME_FONT.get_height() + BLOCK_IMAGE_X_OFFSET
HEALTH_FONT_COLOR = (200, 0, 0)
MONEY_FONT_COLOR = (255, 228, 0)
MONEY_Y_OFFSET = GAME_FONT.get_height()

STAGE_DIMENSIONS = (1200, 760)
STAGE_COLOR = (25, 25, 25)
TRACK_COLOR = (0, 255, 0)
TRACK_THICKNESS = 5

ENEMY_RADIUS = 20
ENEMY_BASE_SPEED = 1
ENEMY_IMAGE_1HP = pygame.transform.scale(pygame.image.load('assets/enemy_1hp.png').convert_alpha(), (2 * ENEMY_RADIUS, 2 * ENEMY_RADIUS))
ENEMY_IMAGE_2HP = pygame.transform.scale(pygame.image.load('assets/enemy_2hp.png').convert_alpha(), (2 * ENEMY_RADIUS, 2 * ENEMY_RADIUS))

PLAYER_MAX_HP = 100