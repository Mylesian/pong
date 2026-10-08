import pygame
from level import (
    track as tr,
    enemy as e
)
import util.timer
import util.button as button
from tower import (
    tower_base
)
from util.constants import (
    screen_constants as sc,
    data_constants as dat,
    stage_constants as stage,
    enemy_constants as enemy,
    player_constants as p,
    projectile_constants as pr
)

# just wave initializing things
spawn_timer_offset: float = 0
with open(dat.WAVES_DATA_PATH) as waves:
    wave_data: list[str] = waves.read().split('\n')

# class to hold all the info about the currently displayed stage
class Stage(pygame.Surface):
    def __init__(this, screen_dimensions, info):
        super().__init__(stage.STAGE_DIMENSIONS)
        this.screen_dimensions = screen_dimensions
        this.info = info
        
        this.current_hp = p.PLAYER_MAX_HP
        this.current_money = p.START_MONEY
        
        this.path = tr.Track(set_points(info.split('|')))
        this.enemies: list[e.Enemy] = []
        this.enemy_timers: list[util.timer.Timer] = []
        this.projectiles: list[tower_base.Projectile] = []
        this.towers: list[tower_base.Tower] = []
        this.restart_button = button.Button(((screen_dimensions[0] - stage.UI_BUTTON_WIDTH) / 2, (screen_dimensions[1] - stage.UI_BUTTON_WIDTH) / 2),
                                            stage.RESTART_BUTTON_IMAGE,
                                            this.restart)
        this.end_screen = False
        
        this.waves = []
        for w in wave_data:
            this.waves.append(w.split('|'))
        
        this.current_wave = 0
        this.wave_in_progress = False
        
        def next_wave():
            global spawn_timer_offset
            spawn_timer_offset = 0
            if this.current_wave < this.waves.__len__():
                this.wave_in_progress = True
                this.make_enemies(this.waves[this.current_wave])
        this.next_wave_button = button.Button((this.get_width() - stage.UI_BUTTON_WIDTH, 0, stage.UI_BUTTON_WIDTH, stage.UI_BUTTON_WIDTH),
                                              stage.WAVE_BUTTON_IMAGE,
                                              next_wave)
        
    # the bulk of the actual frame logic
    # updates all the enemies, timers, projectiles, towers
    # returns itself to be drawn to the screen in the game object
    def update(this, mouse_just_down: bool, dt: float) -> 'Stage':
        this.fill(stage.STAGE_COLOR)
        this.path.draw(this)
        
        if not this.end_screen:
            for t in this.enemy_timers[:]:
                if t.countdown(dt):
                    this.enemy_timers.remove(t)
        
        for t in this.towers:
            if not this.end_screen:
                t.update(dt, this.enemies, mouse_just_down)
            this.blit(t.image, t.pos - (p.TOWER_RADIUS, p.TOWER_RADIUS))
        
        for proj in this.projectiles[:]:
            if not this.end_screen:
                if proj.update(this.enemies):
                    this.projectiles.remove(proj)
            this.blit(proj.image, proj.pos - (pr.PROJECTILE_RADIUS, pr.PROJECTILE_RADIUS))
        
        for e in this.enemies[:]:
            if not e.move_along_track():
                this.enemies.remove(e)
                this.current_hp -= e.hp
            this.blit(e.image, e.pos - (enemy.ENEMY_RADIUS, enemy.ENEMY_RADIUS))

        if not this.end_screen:
            if not this.wave_in_progress:
                this.next_wave_button.update(mouse_just_down)
                this.next_wave_button.draw(this)
            elif this.enemy_timers.__len__() == 0 and this.enemies.__len__() == 0:
                this.wave_in_progress = False
                this.current_money += stage.BASE_WAVE_MONEY_GAIN + this.current_wave * stage.WAVE_MONEY_INCREMENT
                this.current_wave += 1
                
                if this.current_wave == this.waves.__len__():
                    this.win()
            
            if this.current_hp <= 0:
                this.lose()
        
        return this
    
    def restart(this):
        return Stage(this.screen_dimensions, this.info)
    def win(this) -> 'Stage':
        this.end_message = 'Stage Clear!'
        this.end_screen = True
    def lose(this) -> 'Stage':
        this.end_message = 'Stage Failed'
        this.end_screen = True
    
    def make_enemies(this, info: list[str]):
        this.wave_start = True
        global spawn_timer_offset
        for group in info:
            group_info = group.split(',')
            spawn_timer_offset += float(group_info[0])
            
            for i in range(int(group_info[1])):
                if not i == 0:
                    spawn_delay = float(group_info[3])
                else: spawn_delay = 0
                
                en = e.Enemy(int(group_info[2]), this.path, this.enemies)
                this.enemy_timers.append(util.timer.Timer(spawn_timer_offset + spawn_delay, True, en))
                
                spawn_timer_offset += spawn_delay
                
    # get surfaces with player info to write to the screen
    def get_info_block(this) -> pygame.Surface:
        hp_block = sc.GAME_FONT.render(f'{this.current_hp}', False, sc.HEALTH_FONT_COLOR)
        money_block = sc.GAME_FONT.render(f'{this.current_money}', False, sc.MONEY_FONT_COLOR)
        
        return hp_block, money_block
    
def set_points(info: list[str]) -> list[tuple]:
    points: list[tuple] = []
    for line in info:
        pt = line.split(',')
        points.append((int(pt[0]), int(pt[1])))
        
    return points