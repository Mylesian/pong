import pygame
import level.track as track
import util.timer
from tower import tower
from level.enemy import Enemy
from util.constants import (
    data_constants as dat,
    stage_constants as stage,
    enemy_constants as enemy,
    player_constants as p,
    projectile_constants as pr
)

# just wave initializing things
# might be a good idea to make a wave class to store it all during runtime?
spawn_timer_offset: float = 0
with open(dat.WAVES_DATA_PATH) as waves:
    wave_data: list[str] = waves.read().split('|')

# class to hold all the info about the currently displayed stage
class Stage(pygame.Surface):
    def __init__(this, info):
        super().__init__(stage.STAGE_DIMENSIONS)
        
        this.path = track.Track(set_points(info.split('|')))
        this.enemies: list[Enemy] = []
        this.active_timers: list[util.timer.Timer] = []
        this.projectiles: list[tower.Projectile] = []
        this.towers: list[tower.Tower] = []
        
        this.make_enemies(wave_data)
        
        this.towers.append(tower.Tower(this, pygame.math.Vector2(pygame.mouse.get_pos())))
        
    # the bulk of the actual frame logic
    # updates all the enemies, timers, projectiles, towers
    # returns itself to be drawn to the screen in the game object
    def update(this, game, mouse_down: bool, dt: float) -> 'Stage':
        this.fill(stage.STAGE_COLOR)
        this.path.draw(this)
        
        for t in this.active_timers[:]:
            if t.countdown(dt):
                this.active_timers.remove(t)
        
        for t in this.towers:
            t.update(dt, this.enemies, mouse_down)
            this.blit(t.image, t.pos - (p.TOWER_RADIUS, p.TOWER_RADIUS))
        
        for proj in this.projectiles[:]:
            if proj.update(this.enemies):
                this.projectiles.remove(proj)
            this.blit(proj.image, proj.pos - (pr.PROJECTILE_RADIUS, pr.PROJECTILE_RADIUS))
        
        for e in this.enemies[:]:
            if not e.move_along_track():
                this.enemies.remove(e)
                game.current_hp -= e.hp
            this.blit(e.image, e.pos - (enemy.ENEMY_RADIUS, enemy.ENEMY_RADIUS))
        
        return this
    
    def make_enemies(this, info: list[str]):
        global spawn_timer_offset
        for group in info:
            group_info = group.split(',')
            spawn_timer_offset += float(group_info[0])
            
            for i in range(int(group_info[1])):
                spawn_delay = float(group_info[3])
                
                e = Enemy(int(group_info[2]), this.path, this.enemies)
                this.active_timers.append(util.timer.Timer(spawn_timer_offset + spawn_delay, True, e))
                
                spawn_timer_offset += spawn_delay
    
def set_points(info: list[str]) -> list[tuple]:
    points: list[tuple] = []
    for line in info:
        pt = line.split(',')
        points.append((int(pt[0]), int(pt[1])))
        
    return points