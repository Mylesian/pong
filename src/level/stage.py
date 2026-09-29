import pygame
import level.track as track
import util.timer
from level.enemy import Enemy
from util.constants import (
    WAVES_DATA_PATH,
    STAGE_DIMENSIONS,
    STAGE_COLOR,
    ENEMY_RADIUS
)

spawn_timer_offset: float = 0
with open(WAVES_DATA_PATH) as waves:
    wave_data: list[str] = waves.read().split('|')

class Stage(pygame.Surface):
    def __init__(this, info):
        super().__init__(STAGE_DIMENSIONS)
        
        this.path = track.Track(set_points(info.split('|')))
        this.enemies: list[Enemy] = []
        this.active_timers: list[util.timer.Timer] = []
        
        this.make_enemies(wave_data)
        
    def update(this, game, dt: float) -> 'Stage':
        this.fill(STAGE_COLOR)
        this.path.draw(this)
        
        for t in this.active_timers[:]:
            if t.countdown(dt):
                this.active_timers.remove(t)
        
        for e in this.enemies[:]:
            if not e.move_along_track():
                this.enemies.remove(e)
                game.current_hp -= e.hp
            this.blit(e.image, e.pos - (ENEMY_RADIUS, ENEMY_RADIUS))
        
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