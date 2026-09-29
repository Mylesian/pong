import pygame
import level.track as track
import util.timer
from util.constants import (
    ENEMY_BASE_SPEED,
    ENEMY_IMAGE_1HP,
    ENEMY_IMAGE_2HP
)

class Enemy(util.timer.Dependent):
    def __init__(this, max_hp: int, path: track.Track,  dest: list['Enemy']):
        this.max_hp = max_hp
        this.hp = max_hp
        this.set_image()
        this.path = path
        this.pos = pygame.math.Vector2(path.points[0][0], path.points[0][1])
        this.target_pos = 1
        this.set_velocity()
        
        this.dest = dest
    
    def move_along_track(this):
        if ((this.pos - this.path.points[this.target_pos - 1]).magnitude_squared() >
           (this.path.points[this.target_pos] - this.path.points[this.target_pos - 1]).magnitude_squared()):
            this.pos = pygame.math.Vector2(this.path.points[this.target_pos])
            this.target_pos += 1
            
            if this.target_pos >= this.path.points.__len__():
                return False
            
            this.set_velocity()
            
        this.pos += this.velocity
        return True
        
    def set_velocity(this):
        vel = this.path.points[this.target_pos] - this.pos
        this.velocity = vel / vel.magnitude() * ENEMY_BASE_SPEED * this.hp
        
    def set_image(this):
        match this.hp:
            case 1:
                this.image = ENEMY_IMAGE_1HP
            case 2:
                this.image = ENEMY_IMAGE_2HP
    
    def update(this):
        this.dest.append(this)